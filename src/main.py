import os
import ffmpeg
from kombu import Queue
from flask import Flask
from celery import Celery

from src.config import Config
from src.s3_client import S3Client
from src.rabbitmq_client import RabbitMQClient
from src.file_client import FileClient
from src.converter import ProtobufConverter
from src.Protobuf.Message_pb2 import ApiToSubtitleIncrustator, MediaPodStatus, Video, MediaPod

app = Flask(__name__)
app.config.from_object(Config)
s3_client = S3Client(Config)
rmq_client = RabbitMQClient()
file_client = FileClient()

celery = Celery(
    'tasks',
    broker=app.config['RABBITMQ_URL']
)

celery.conf.update({
    'task_serializer': 'json',
    'accept_content': ['json'],
    'broker_connection_retry_on_startup': True,
    'task_routes': {
        'tasks.process_message': {'queue': app.config['RMQ_QUEUE_WRITE']}
    },
    'task_queues': [
        Queue(app.config['RMQ_QUEUE_READ'], routing_key=app.config['RMQ_QUEUE_READ'])
    ],
})

@celery.task(name='tasks.process_message', queue=app.config['RMQ_QUEUE_READ'])
def process_message(message):
    mediaPod: MediaPod = ProtobufConverter.json_to_protobuf(message)
    protobuf = ApiToSubtitleIncrustator()
    protobuf.mediaPod.CopyFrom(mediaPod)
    protobuf.IsInitialized()

    try:
        uuid = os.path.splitext(protobuf.mediaPod.originalVideo.name)[0]
        type = os.path.splitext(protobuf.mediaPod.originalVideo.name)[1]

        keyAss = f"{protobuf.mediaPod.userUuid}/{protobuf.mediaPod.uuid}/{protobuf.mediaPod.processedVideo.ass}"
        keyVideo = f"{protobuf.mediaPod.userUuid}/{protobuf.mediaPod.uuid}/{protobuf.mediaPod.processedVideo.name}"
        keyVideoProcessed = f"{protobuf.mediaPod.userUuid}/{protobuf.mediaPod.uuid}/{uuid}_processed{type}"

        tmpVideoFilePath = f"/tmp/{uuid}{type}"
        tmpProcessedVideoFilePath = f"/tmp/{uuid}_processed{type}"
        tmpAssFilePath = f"/tmp/{uuid}.ass"

        if not s3_client.download_file(keyAss, tmpAssFilePath):
            raise Exception

        if not s3_client.download_file(keyVideo, tmpVideoFilePath):
            raise Exception
        
        ffmpeg.input(tmpVideoFilePath).output(
            tmpProcessedVideoFilePath, 
            vf=f"subtitles={tmpAssFilePath}",
            vcodec="libx264", crf=23, preset="fast",
        ).run()

        if not s3_client.upload_file(tmpProcessedVideoFilePath, keyVideoProcessed):
            raise Exception
        
        protobuf.mediaPod.status = MediaPodStatus.Name(MediaPodStatus.SUBTITLE_INCRUSTATOR_COMPLETE)

        file_client.delete_file(tmpAssFilePath)
        file_client.delete_file(tmpProcessedVideoFilePath)
        file_client.delete_file(tmpVideoFilePath)

        rmq_client.send_message(protobuf, "App\\Protobuf\\SubtitleIncrustatorToApi")
    except Exception as e:
        protobuf.mediaPod.status = MediaPodStatus.Name(MediaPodStatus.SUBTITLE_INCRUSTATOR_ERROR)
        if not rmq_client.send_message(protobuf, "App\\Protobuf\\SubtitleIncrustatorToApi"):
            return False
