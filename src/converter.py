import json
from src.Protobuf.Message_pb2 import ApiToSubtitleIncrustator, MediaPod, Video

class ProtobufConverter:
    @staticmethod
    def json_to_protobuf(message: str) -> ApiToSubtitleIncrustator:
        data = json.loads(message)
        media_pod_data = data["mediaPod"]

        video = Video()
        video.name = media_pod_data["originalVideo"]["name"]
        video.mimeType = media_pod_data["originalVideo"]["mimeType"]
        video.size = int(media_pod_data["originalVideo"]["size"])
        video.audios.extend(media_pod_data["originalVideo"]["audios"])
        video.subtitles.extend(media_pod_data["originalVideo"]["subtitles"])
        
        media_pod = MediaPod()
        media_pod.uuid = media_pod_data["uuid"]
        media_pod.userUuid = media_pod_data["userUuid"]
        media_pod.status = media_pod_data["status"]
        media_pod.originalVideo.CopyFrom(video)

        proto_message = ApiToSubtitleIncrustator()
        proto_message.mediaPod.CopyFrom(media_pod)

        return proto_message
