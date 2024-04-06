import enum
import json
import os.path

from typing import Optional

from compress.compressor import CompressService
from logic.client import TcpClient


class VcClient(TcpClient):
    """
    VcClient is the client class for video compressor service.
    This has custom tcp-based protocol named MMP.
    VideoCompressor/MMP.txt is the file path that describes MMP.
    """

    def __init__(self, server_address: str, server_port: int) -> None:
        super().__init__(server_address, server_port)
        self.header_size = 64

    # Override TcpClient.upload()
    def upload(self) -> None:
        # Upload anything
        super()._connect_with_server()
        self.__get_user_input()
        self.__send_header()
        self.__send_json()
        self.__send_media_type()
        self.__send_payload()

    def compress_service_start(self):
        # Start compress service
        while True:
            selected_service = input("Please select a service from 1 to 5...\n"
                                     "1 --> Compress video file.\n"
                                     "2 --> Change video resolution.\n"
                                     "3 --> Change the video aspect ratio.\n"
                                     "4 --> Convert video to audio.\n"
                                     "5 --> Create Gif from video.\n")
            # Todo not a number case should be handled
            if int(selected_service) < CompressService.Compress.value or \
                    int(selected_service) > CompressService.Create_Gif.value:
                print("You should select from 1 to 5.")
                continue
            break

        self.compress_service_parsed_json = self.__parse_compress_service_detail_json(
            CompressService.get_service(selected_service))
        self.sock.send(self.compress_service_parsed_json.encode())

    def __parse_compress_service_detail_json(self, select_service: enum.Enum) -> Optional[str]:
        json_data = None
        if select_service == CompressService.Compress:
            json_data = self.__parse_compress_json()
        elif select_service == CompressService.Change_Resolution:
            json_data = self.__parse_change_resolution_json()
        elif select_service == CompressService.Change_Aspect_Ratio:
            json_data = self.__parse_change_aspect_ratio_json()
        elif select_service == CompressService.Convert_Into_Audio:
            json_data = self.__parse_convert_into_audio_json()
        elif select_service == CompressService.Create_Gif:
            json_data = self.__parse_create_gif_json()
        else:
            print("No such service.")
            self.logger.error("No such compress service we provide: __parse_compress_service_detail_json().")
            raise Exception("No such service.")

        return json_data

    def __parse_compress_json(self) -> str:
        def __get_compress_level() -> str:
            return input('Please select the degree of compression\n'
                         'low\n'
                         'medium\n'
                         'high\n')

        compress_json_data = {
            "service": CompressService.Compress.value,
            "level": __get_compress_level(),
        }
        return json.dumps(compress_json_data)

    def __parse_change_resolution_json(self):
        def __get_height():
            return input("Please input height (ex:1280):")

        def __get_width():
            return input("Please input weight (ex:720):")

        change_resolution_data = {
            "service": CompressService.Change_Resolution.value,
            "height": __get_height(),
            "width": __get_width()
        }
        return json.dumps(change_resolution_data)

    def __parse_change_aspect_ratio_json(self):
        def __get_height_ratio():
            return input("Please enter the height rate(ex:16):")

        def __get_width_ratio():
            return input("Please enter the width rate(ex:9)")

        height_ratio = __get_height_ratio()
        width_ratio = __get_width_ratio()

        change_aspect_ratio = {
            "service": CompressService.Change_Aspect_Ratio.value,
            "height_ratio": height_ratio,
            "width_ratio": width_ratio,
        }
        return json.dumps(change_aspect_ratio)

    def __parse_convert_into_audio_json(self):
        return json.dumps({
            "service": CompressService.Convert_Into_Audio.value,
        })

    def __parse_create_gif_json(self):
        start = input('Input start position (ex. 00:00:20): ')
        end = input('Input end position (ex. 10): ')
        flame_rate = input('Input flame rate (ex. 10): ')
        resize = input('Input resize (ex. 300): ')
        return json.dumps({
            "service": CompressService.Create_Gif.value,
            "start": start,
            "end": end,
            "flame_rate": flame_rate,
            "resize": resize,
        })

    def __get_user_input(self) -> None:
        """
        TODO
        Parse json, media_type, payload
        Also, get all layer's sizes.

        When parse json, we should know payload's filename and payload's filesize
        So, json would be like this.
        {
            filename: hogehoge: str
            filesize: foobar: int
        }
        """
        self.__get_payload_filename()
        self.__read_payload_file()

    def __get_payload_filename(self) -> None:
        self.payload_filepath = input("Enter absolute filepath that you wanna compress with this service.")
        self.payload_filename = os.path.basename(self.payload_filepath)
        self.media_type = os.path.splitext(self.payload_filepath)[1]
        # TODO
        # extension validation

    def __read_payload_file(self) -> None:
        with open(self.payload_filepath, "rb+") as payload_file:
            self.__get_payload_size()
            self.__parse_json()

    def __parse_json(self) -> None:
        # TODO
        # Is self.json_path correct ?
        self.json_path = os.path.abspath("data.json")
        payload_data = {
            "payload_filename": self.payload_filename,
            "payload_filesize": self.payload_filesize
        }
        # TODO
        # Is file mode correct ?
        with open(self.json_path, "w+") as json_file:
            json.dump(payload_data, json_file)

    def __send_header(self) -> None:
        self.sock.send(self.__make_mmp_header())

    def __send_json(self) -> None:
        with open(self.json_path, "r+") as json_file:
            data_length = self.json_filesize
            data = json_file.read(data_length if data_length < self.stream_rate else self.stream_rate)
            while data:
                self.sock.send(data.encode())
                data_length -= len(data)
                data = json_file.read(data_length if data_length < self.stream_rate else self.stream_rate)
        os.remove(self.json_path)
        self.logger.debug("Success to upload json file.")

    def __send_media_type(self) -> None:
        self.sock.send(self.media_type.encode())
        self.logger.debug("Success to upload media type.")

    def __send_payload(self) -> None:
        with open(self.payload_filepath, "rb+") as payload_file:
            data_length = self.payload_filesize
            data = payload_file.read(data_length if data_length < self.stream_rate else self.stream_rate)
            while data:
                self.sock.send(data)
                data_length -= len(data)
                data = payload_file.read(data_length if data_length < self.stream_rate else self.stream_rate)
        self.logger.debug("Success to upload payload file.")

    def __make_mmp_header(self) -> bytes:
        print("Payload_filesize: ", self.__get_payload_size())
        header = self.__get_json_size().to_bytes(16, "big") \
                 + len(self.media_type).to_bytes(1, "big") + self.__get_payload_size().to_bytes(47, "big")
        print(header)
        return header

    def __get_json_size(self) -> int:
        with open(self.json_path, "r+") as json_file:
            self.json_filesize = super()._get_filesize(json_file)
        return self.json_filesize

    def __get_payload_size(self) -> int:
        with open(self.payload_filepath, "r+") as payload_file:
            self.payload_filesize = super()._get_filesize(payload_file)
        return self.payload_filesize


if __name__ == '__main__':
    vc_client = VcClient("0.0.0.0", 5001)
    vc_client.upload()
    vc_client.compress_service_start()
