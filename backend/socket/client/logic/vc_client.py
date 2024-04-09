import json
import os.path

from typing import Optional, Any

from compress.compressor import CompressService
from compress.serviceResult import ServiceResult2
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
        self.srp_return_code_size = 1
        self.srp_file_content_size = 1024
        self.srp_mime_type_size = 15
        self.srp_header_size = self.srp_return_code_size + self.srp_file_content_size + self.srp_mime_type_size
        self.payload_filename = payload_filename
        self.payload_dirpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw")
        self.payload_filepath = os.path.join(self.payload_dirpath, self.payload_filename)

    # Override TcpClient.upload()
    def upload(self) -> None:
        # Upload anything
        super()._connect_with_server()
        self.__read_payload_file()
        self.__send_header()
        self.__send_json()
        self.__send_media_type()
        self.__send_payload()

    def compress_service_start(self, request_json: dict) -> ServiceResult2:
        self.compress_service_parsed_json = self.__parse_compress_service_detail_json(request_json)
        self.sock.send(self.compress_service_parsed_json.encode())
        service_result_header = self.sock.recv(self.srp_header_size)
        service_result_return_code = int.from_bytes(service_result_header[:self.srp_return_code_size], "big")
        service_result_content_size = int.from_bytes(service_result_header[self.srp_return_code_size:self.srp_return_code_size + self.srp_file_content_size], "big")
        service_result_mime_type_size = int.from_bytes(service_result_header[self.srp_return_code_size + self.srp_file_content_size:], "big")
        file_content = self.__get_file_content(service_result_content_size)
        mime_type = self.__get_mime_type(service_result_mime_type_size)
        print("MIME_type >>", mime_type)
        return ServiceResult2(service_result_return_code, file_content, mime_type)

    def __get_file_content(self, file_size) -> bytes:
        data_size = file_size
        data = self.sock.recv(self.stream_rate)
        data_size -= len(data)
        while data_size > 0:
            current_data = self.sock.recv(data_size if data_size < self.stream_rate else self.stream_rate)
            data_size -= len(current_data)
            data += current_data
        return data

    def __get_mime_type(self, mime_type_size: int) -> str:
        return self.sock.recv(self.stream_rate).decode('utf-8')

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
