import json
import logging
import subprocess

from compress.compress_service import CompressService


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
        self.__load_compress_service_json()

    def __load_compress_service_json(self):
        self.compress_service_loaded_data = json.loads(self.compress_service_json)
        self.__set_service()

    def __set_service(self):
        self.service = CompressService.get_service(self.compress_service_loaded_data["service"])

    def run(self) -> None:
        def _run():
            self.command = self.command.split(" ")
            subprocess.run(self.command)

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
            self.__convert_into_audio()

        elif self.service == CompressService.Create_Gif:
            self.logger.debug("Do create gif service start: numbers is 5")
            self.__create_gif()

        else:
            self.logger.debug("No such service. Error has been occured.")
            raise Exception("No such service")

        _run()

    def __compress(self):
        level = self.compress_service_loaded_data["level"]
        if level == "low":
            self.option = " -c:v libx264 data/compress_low.mp4"
        elif level == "medium":
            self.option = " -c:v libx265 data/compress_medium.mp4"
        elif level == "high":
            self.option = " -c:v libx265 -b:v 500k data/compress_high.mp4"
        else:
            raise Exception("No such compress level")
        self.command = self.base_command + self.option

    def __change_resolution(self):
        height = self.compress_service_loaded_data["height"]
        width = self.compress_service_loaded_data["width"]
        self.option = " -filter:v scale=" + height + ":" + width + " -c:a copy data/change_resolution.mp4"
        self.command = self.base_command + self.option

    def __change_aspect_ratio(self):
        height_ratio = self.compress_service_loaded_data["height_ratio"]
        width_ratio = self.compress_service_loaded_data["width_ratio"]
        self.option = ' -pix_fmt yuv420p -aspect ' + height_ratio + ':' + width_ratio + ' data/change_aspect.mp4'
        self.command = self.base_command + self.option

    def __convert_into_audio(self):
        self.option = " -vn data/convert_into_audio.mp3"
        self.command = self.base_command + self.option

    def __create_gif(self):
        start = self.compress_service_loaded_data["start"]
        end = self.compress_service_loaded_data["end"]
        flame_rate = self.compress_service_loaded_data["flame_rate"]
        resize = self.compress_service_loaded_data["resize"]
        self.command = 'ffmpeg -ss ' + start + ' -i ' + self.payload_filename + ' -to ' + end + ' -r ' + flame_rate + ' -vf scale=' + resize + ':-1 data/create_gif.gif'
