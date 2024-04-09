import json
import logging
import os.path
import subprocess

from compress.compress_service import CompressService
from compress.serviceResult import ServiceResult


class Compressor(object):
    def __init__(self, compress_service_json: str, payload_filename: str):
        logging.basicConfig(level=logging.DEBUG, filename="compressor.log", filemode='w')
        self.logger = logging.getLogger()
        self.service = None
        self.compress_service_loaded_data = None
        self.command = None
        self.option = None
        self.compress_service_json = compress_service_json
        self.payload_filename = payload_filename
        self.base_command = "ffmpeg -i " + self.payload_filename
        self.output_filename = None
        self.output_mime_type = "video/mp4"
        self.__load_compress_service_json()

    def __load_compress_service_json(self):
        self.compress_service_loaded_data = json.loads(self.compress_service_json)
        self.__set_service()

    def __set_service(self):
        self.service = CompressService.get_service(self.compress_service_loaded_data["service"])

    def run(self) -> ServiceResult:
        def _run() -> ServiceResult:
            self.command = self.command.split(" ")
            result = subprocess.run(self.command)
            output_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.output_filename)
            print("MIME MIME>>", self.output_mime_type)
            return ServiceResult(result, output_filepath, self.output_mime_type)

        if self.service == CompressService.Compress:
            self.logger.debug("Do compress service start: numbers is 1")
            self.__compress()

        elif self.service == CompressService.Change_Resolution:
            self.logger.debug("Do change resolution service start: numbers is 2")
            self.__change_resolution()

        elif self.service == CompressService.Change_Aspect_Ratio:
            self.logger.debug("Do change aspect ratio service start: numbers is 3")
            self.__change_aspect_ratio()

        elif self.service == CompressService.Convert_Into_Audio:
            self.logger.debug("Do convert into audio service start: numbers is 4")
            self.output_mime_type = "audio/mpeg"
            self.__convert_into_audio()

        elif self.service == CompressService.Create_Gif:
            self.logger.debug("Do create gif service start: numbers is 5")
            self.output_mime_type = "image/gif"
            self.__create_gif()

        else:
            self.logger.debug("No such service. Error has been occured.")
            raise Exception("No such service")

        return _run()

    def __compress(self):
        level = self.compress_service_loaded_data["level"]
        if level == "low":
            self.output_filename = "data/compress_low.mp4"
            self.option = " -c:v libx264 " + self.output_filename
        elif level == "medium":
            self.output_filename = "data/compress_medium.mp4"
            self.option = " -c:v libx265 " + self.output_filename
        elif level == "high":
            self.output_filename = "data/compress_high.mp4"
            self.option = " -c:v libx265 -b:v 500k " + self.output_filename
        else:
            raise Exception("No such compress level")
        self.command = self.base_command + self.option

    def __change_resolution(self):
        height = self.compress_service_loaded_data["height"]
        width = self.compress_service_loaded_data["width"]
        self.output_filename = "data/change_resolution.mp4"
        self.option = " -filter:v scale=" + height + ":" + width + " -c:a copy " + self.output_filename
        self.command = self.base_command + self.option

    def __change_aspect_ratio(self):
        height_ratio = self.compress_service_loaded_data["height_ratio"]
        width_ratio = self.compress_service_loaded_data["width_ratio"]
        self.output_filename = "data/change_aspect.mp4"
        self.option = ' -pix_fmt yuv420p -aspect ' + height_ratio + ':' + width_ratio + " " + self.output_filename
        self.command = self.base_command + self.option

    def __convert_into_audio(self):
        self.output_filename = "data/convert_into_audio.mp3"
        self.option = " -vn " + self.output_filename
        self.command = self.base_command + self.option

    def __create_gif(self):
        start = self.compress_service_loaded_data["start_time"]
        end = self.compress_service_loaded_data["end_position"]
        flame_rate = self.compress_service_loaded_data["flame_rate"]
        resize = self.compress_service_loaded_data["resize"]
        self.output_filename = "data/create_gif.gif"
        self.command = 'ffmpeg -ss ' + start + ' -i ' + self.payload_filename + ' -to ' + end + ' -r ' + flame_rate + ' -vf scale=' + resize + ':-1 ' + self.output_filename
