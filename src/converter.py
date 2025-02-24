import json
from src.Protobuf.Message_pb2 import MediaPod, Video, Preset

class ProtobufConverter:
    @staticmethod
    def json_to_protobuf(message: str) -> MediaPod:
        data = json.loads(message)
        media_pod_data = data["mediaPod"]

        media_pod = MediaPod()
        media_pod.uuid = media_pod_data["uuid"]
        media_pod.userUuid = media_pod_data["userUuid"]
        media_pod.format = media_pod_data["format"]

        video = Video()
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

            if "name" in media_pod_data["processedVideo"]:
                processed_video.name = media_pod_data["processedVideo"]["name"]

            if "mimeType" in media_pod_data["processedVideo"]:
                processed_video.mimeType = media_pod_data["processedVideo"]["mimeType"]

            if "size" in media_pod_data["processedVideo"]:
                processed_video.size = int(media_pod_data["processedVideo"]["size"])

            if "length" in media_pod_data["processedVideo"]:
                processed_video.length = int(media_pod_data["processedVideo"]["length"])

            if "audios" in media_pod_data["processedVideo"]:
                processed_video.audios.extend(media_pod_data["processedVideo"]["audios"])

            if "subtitles" in media_pod_data["processedVideo"]:
                processed_video.subtitles.extend(media_pod_data["processedVideo"]["subtitles"])

            if "ass" in media_pod_data["processedVideo"]:
                processed_video.ass = media_pod_data["processedVideo"]["ass"]

            if "subtitle" in media_pod_data["processedVideo"]:
                processed_video.subtitle = media_pod_data["processedVideo"]["subtitle"]

            processed_video.IsInitialized()
            media_pod.processedVideo.CopyFrom(processed_video)

        preset = Preset()
        preset.subtitleFont = media_pod_data["preset"]["subtitleFont"]
        preset.subtitleSize = media_pod_data["preset"]["subtitleSize"]
        preset.subtitleColor = media_pod_data["preset"]["subtitleColor"]
        preset.subtitleBold = media_pod_data["preset"]["subtitleBold"]
        preset.subtitleItalic = media_pod_data["preset"]["subtitleItalic"]
        preset.subtitleUnderline = media_pod_data["preset"]["subtitleUnderline"]
        preset.subtitleOutlineColor = media_pod_data["preset"]["subtitleOutlineColor"]
        preset.subtitleOutlineThickness = media_pod_data["preset"]["subtitleOutlineThickness"]
        preset.subtitleShadow = media_pod_data["preset"]["subtitleShadow"]
        preset.subtitleShadowColor = media_pod_data["preset"]["subtitleShadowColor"]

        preset.IsInitialized()

        media_pod.preset.CopyFrom(preset)

        media_pod.IsInitialized()

        return media_pod
