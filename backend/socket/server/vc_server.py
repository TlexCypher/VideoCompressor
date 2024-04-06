import json
import os.path
import sys

from compress.compressor import Compressor
from server import TcpServer


class VcServer(TcpServer):
    """
    VcClient is the server class for video compressor service.
    This has custom tcp-based protocol named MMP.
    VideoCompressor/MMP.txt is the file path that describes MMP.
    """

    def __init__(self, server_address: str, server_port: int) -> None:
        super().__init__(server_address, server_port)
        self.json_length = 16
        self.media_type_length = 1
        self.payload_length = 47
        self.header_length = self.json_length + self.media_type_length + self.payload_length

        self.json_filename = "data.json"
        self.video_basename = "video"

    def start(self) -> None:
        try:
            while True:
                self.__accept()
                self.__run_compress_service()

        except TimeoutError:
            super().logger.info("No data from client\nClosing connection.")
            sys.exit(1)

    def __accept(self):
        super()._establish_connection()
        self.header = self.connection.recv(self.header_length)
        json_file_length = int.from_bytes(self.header[:self.json_length], "big")
        media_type_length = int.from_bytes(
            self.header[self.json_length:self.json_length + self.media_type_length], "big")
        payload_length = int.from_bytes(self.header[self.json_length + self.media_type_length:], "big")
        print("Option JSON File size => {}, Media type file size => {}, Payload size => {}".format(
            json_file_length,
            media_type_length,
            payload_length))
        self.__accept_json(json_file_length)
        self.__accept_media_type(media_type_length)
        self.__accept_payload(payload_length)

    def __run_compress_service(self):
        compress_service_json = self.connection.recv(self.stream_rate).decode()
        compressor = Compressor(compress_service_json, self.__get_server_data_path(self.payload_filename))
        compressor.run()

    def __accept_json(self, json_file_length: int) -> None:
        return self.__accept_helper(json_file_length, self.json_filename)

    def __accept_media_type(self, media_type_length: int) -> None:
        self.media_type = self.connection.recv(media_type_length).decode()
        return self.media_type

    def __accept_payload(self, payload_length: int) -> None:
        self.payload_filename = self.__get_payload_filename_without_ext(self.__get_server_data_path(self.json_filename)) + self.media_type
        return self.__accept_helper(payload_length, self.payload_filename)

    def __accept_helper(self, file_length: int, filename: str):
        data_length = file_length
        with open(self.__get_server_data_path(filename), "wb+") as f:
            data = self.connection.recv(data_length if data_length < self.stream_rate else self.stream_rate)
            while data:
                f.write(data)
                data_length -= len(data)
                data = self.connection.recv(data_length if data_length < self.stream_rate else self.stream_rate)
        self.logger.debug("Success to upload with __accept_helper()")

    def __get_payload_filename_without_ext(self, json_absolute_filepath: str) -> str:
        with open(json_absolute_filepath, "rb+") as json_file:
            payload_data = json.load(json_file)
            return os.path.splitext(payload_data["payload_filename"])[0]

    def __get_server_data_path(self, filename: str) -> str:
        return os.path.abspath(self.dpath) + "/" + filename


if __name__ == '__main__':
    vc_server = VcServer("0.0.0.0", 5001)
    vc_server.start()
