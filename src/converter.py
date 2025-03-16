import json
from src.Protobuf.Message_pb2 import MediaPod, Video, Configuration


class ProtobufConverter:
    @staticmethod
    def json_to_protobuf(message: str) -> MediaPod:
        data = json.loads(message)
        media_pod_data = data["mediaPod"]

        media_pod = MediaPod()
        media_pod.uuid = media_pod_data["uuid"]
        media_pod.userUuid = media_pod_data["userUuid"]
        
        if "frame" in media_pod_data:
            media_pod.frame = media_pod_data["frame"]

        video = Video()
        video.uuid = media_pod_data["originalVideo"]["uuid"]
        video.name = media_pod_data["originalVideo"]["name"]
        video.mimeType = media_pod_data["originalVideo"]["mimeType"]
        video.size = int(media_pod_data["originalVideo"]["size"])

        if "length" in media_pod_data["originalVideo"]:
            video.length = int(media_pod_data["originalVideo"]["length"])

        if "audios" in media_pod_data["originalVideo"]:
            video.audios.extend(media_pod_data["originalVideo"]["audios"])

        if "subtitles" in media_pod_data["originalVideo"]:
            video.subtitles.extend(media_pod_data["originalVideo"]["subtitles"])

        if "ass" in media_pod_data["originalVideo"]:
            video.ass = media_pod_data["originalVideo"]["ass"]

        if "subtitle" in media_pod_data["originalVideo"]:
            video.subtitle = media_pod_data["originalVideo"]["subtitle"]

        video.IsInitialized()
        media_pod.originalVideo.CopyFrom(video)

        if "processedVideo" in media_pod_data:
            processed_video = Video()
            processed_video.uuid = media_pod_data["processedVideo"]["uuid"]

            if "name" in media_pod_data["processedVideo"]:
                processed_video.name = media_pod_data["processedVideo"]["name"]

            if "mimeType" in media_pod_data["processedVideo"]:
                processed_video.mimeType = media_pod_data["processedVideo"]["mimeType"]

            if "size" in media_pod_data["processedVideo"]:
                processed_video.size = int(media_pod_data["processedVideo"]["size"])

            if "length" in media_pod_data["processedVideo"]:
                processed_video.length = int(media_pod_data["processedVideo"]["length"])

            if "audios" in media_pod_data["processedVideo"]:
                processed_video.audios.extend(
                    media_pod_data["processedVideo"]["audios"]
                )

            if "subtitles" in media_pod_data["processedVideo"]:
                processed_video.subtitles.extend(
                    media_pod_data["processedVideo"]["subtitles"]
                )

            if "ass" in media_pod_data["processedVideo"]:
                processed_video.ass = media_pod_data["processedVideo"]["ass"]

            if "subtitle" in media_pod_data["processedVideo"]:
                processed_video.subtitle = media_pod_data["processedVideo"]["subtitle"]

            processed_video.IsInitialized()
            media_pod.processedVideo.CopyFrom(processed_video)

        if "finalVideo" in media_pod_data:
            for video in media_pod_data["finalVideo"]:
                final_video = Video()
                final_video.uuid = video["uuid"]
                final_video.name = video["name"]
                final_video.mimeType = video["mimeType"]
                final_video.size = int(video["size"])
                final_video.length = int(video["length"])
                final_video.IsInitialized()
                media_pod.finalVideo.append(final_video)

        configuration = Configuration()
        configuration.subtitleFont = media_pod_data["configuration"]["subtitleFont"]
        configuration.subtitleSize = media_pod_data["configuration"]["subtitleSize"]
        configuration.subtitleColor = media_pod_data["configuration"]["subtitleColor"]
        configuration.subtitleBold = media_pod_data["configuration"]["subtitleBold"]
        configuration.subtitleItalic = media_pod_data["configuration"]["subtitleItalic"]
        configuration.subtitleUnderline = media_pod_data["configuration"][
            "subtitleUnderline"
        ]
        configuration.subtitleOutlineColor = media_pod_data["configuration"][
            "subtitleOutlineColor"
        ]
        configuration.subtitleOutlineThickness = media_pod_data["configuration"][
            "subtitleOutlineThickness"
        ]
        configuration.subtitleShadow = media_pod_data["configuration"]["subtitleShadow"]
        configuration.subtitleShadowColor = media_pod_data["configuration"][
            "subtitleShadowColor"
        ]
        configuration.format = media_pod_data["configuration"]["format"]
        configuration.split = media_pod_data["configuration"]["split"]

        configuration.IsInitialized()

        media_pod.configuration.CopyFrom(configuration)

        media_pod.IsInitialized()

        return media_pod
