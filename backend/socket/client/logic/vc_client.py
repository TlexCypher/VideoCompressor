import enum
import json
import os.path

from typing import Optional, Any

from compress.compressor import CompressService
from logic.client import TcpClient


class VcClient(TcpClient):
    """
    VcClient is the client class for video compressor service.
    This has custom tcp-based protocol named MMP.
    VideoCompressor/MMP.txt is the file path that describes MMP.
    """

    def __init__(self, server_address: str, server_port: int, payload_filename: str) -> None:
        super().__init__(server_address, server_port)
        self.header_size = 64
        self.payload_filename = payload_filename
        self.payload_dirpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'server/raw/')
        self.payload_filepath = os.path.join(self.payload_dirpath, self.payload_filename)
        print("###############################")
        print("payload directory path,", self.payload_dirpath)
        print("payload file path", self.payload_filepath)
        print("payload file name", self.payload_filename)

    # Override TcpClient.upload()
    def upload(self) -> None:
        # Upload anything
        super()._connect_with_server()
        self.__read_payload_file()
        self.__send_header()
        self.__send_json()
        self.__send_media_type()
        self.__send_payload()

    def compress_service_start(self, request_json: dict) -> int:
        self.compress_service_parsed_json = self.__parse_compress_service_detail_json(request_json)
        self.sock.send(self.compress_service_parsed_json.encode())
        service_result = int.from_bytes(self.sock.recv(self.stream_rate), "big")
        return service_result

    def __parse_compress_service_detail_json(self, request_json: dict) -> Optional[str]:
        def __get_number_expression(_service: str) -> Optional[int]:
            if _service == "Compress":
                return 1
            elif _service == "Change resolution":
                return 2
            elif _service == "Change aspect ratio":
                return 3
            elif _service == "Convert into audio":
                return 4
            elif _service == "Create gif":
                return 5
            else:
                self.logger.error("No such service in {}, __parse_compress_service_detail_json()".format(__file__))
                raise Exception("No such service")

        json_data = None
        _service = request_json["service"]
        service = __get_number_expression(_service)
        print("_SERVICE", _service)
        if service == CompressService.Compress.value:
            json_data = self.__parse_compress_json(request_json)
        elif service == CompressService.Change_Resolution.value:
            json_data = self.__parse_change_resolution_json(request_json)
        elif service == CompressService.Change_Aspect_Ratio.value:
            json_data = self.__parse_change_aspect_ratio_json(request_json)
        elif service == CompressService.Convert_Into_Audio.value:
            json_data = self.__parse_convert_into_audio_json()
        elif service == CompressService.Create_Gif.value:
            json_data = self.__parse_create_gif_json(request_json)
        else:
            print("No such service.")
            self.logger.error("No such compress service we provide: __parse_compress_service_detail_json().")
            raise Exception("No such service.")

        return json_data

    def __parse_compress_json(self, request_json: dict) -> str:
        return json.dumps({
            "service": CompressService.Compress.value,
            "level": request_json["level"],
        })

    def __parse_change_resolution_json(self, request_json: dict):
        return json.dumps({
            "service": CompressService.Change_Resolution.value,
            "height": request_json["height"],
            "width": request_json["width"]
        })

    def __parse_change_aspect_ratio_json(self, request_json: dict):
        return json.dumps({
            "service": CompressService.Change_Aspect_Ratio.value,
            "height_ratio": request_json["height_ratio"],
            "width_ratio": request_json["width_ratio"],
        })

    def __parse_convert_into_audio_json(self):
        return json.dumps({
            "service": CompressService.Convert_Into_Audio.value,
        })

    def __parse_create_gif_json(self, request_json: dict):
        return json.dumps({
            "service": CompressService.Create_Gif.value,
            "start_time": request_json["start_time"],
            "end_position": request_json["end_position"],
            "flame_rate": request_json["flame_rate"],
            "resize": request_json["resize"],
        })

    def __get_media_type(self) -> None:
        self.media_type = os.path.splitext(self.payload_filepath)[1]
        # TODO
        # extension validation

    def __read_payload_file(self) -> None:
        self.__get_media_type()
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
