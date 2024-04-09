import json
import os.path
import shutil
import sys

from compress.compressor import Compressor
from compress.serviceResult import ServiceResult
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

    def start(self) -> ServiceResult:
        try:
            while True:
                self.__accept()
                subprocess = self.__run_compress_service()
                if subprocess.result.returncode == 0:
                    self.logger.info("Success to end service.")
                else:
                    self.logger.error("Something wrong was happened. Failed to end service")
                return subprocess

        except TimeoutError:
            super().logger.info("No data from client\nClosing connection.")
            sys.exit(1)

    @staticmethod
    def clean():
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        raw_dir = os.path.join(os.path.dirname(__file__), "raw")

        if os.path.exists(data_dir):
            os.chmod(data_dir, 0o777)
            shutil.rmtree(data_dir)

        if os.path.exists(raw_dir):
            os.chmod(raw_dir, 0o777)
            shutil.rmtree(raw_dir)

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

    def __run_compress_service(self) -> ServiceResult:
        compress_service_json = self.connection.recv(self.stream_rate).decode()
        compressor = Compressor(compress_service_json, self.__get_server_data_path(self.payload_filename))
        return compressor.run()

    def __accept_json(self, json_file_length: int) -> None:
        return self.__accept_helper(json_file_length, self.json_filename)

    def __accept_media_type(self, media_type_length: int) -> None:
        self.media_type = self.connection.recv(media_type_length).decode()
        return self.media_type

    def __accept_payload(self, payload_length: int) -> None:
        self.payload_filename = self.__get_payload_filename_without_ext(
            self.__get_server_data_path(self.json_filename)) + self.media_type
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


def __make_srp_protocol_header(service_result: ServiceResult):
    data = read_as_binary(service_result.output_filepath)
    return service_result.result.returncode.to_bytes(1, "big") + len(data).to_bytes(1024, "big") \
        + len(service_result.mime_type).to_bytes(15, "big")


def read_as_binary(output_filepath: str) -> bytes:
    stream_rate = 1024
    with open(output_filepath, "rb+") as f:
        f.seek(0, 0)
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0, 0)

        data = f.read(stream_rate)
        file_size -= len(data)

        while file_size > 0:
            current_data = f.read(file_size if file_size < stream_rate else stream_rate)
            file_size -= len(current_data)
            data += current_data
        return data


if __name__ == '__main__':
    VcServer.clean()
    vc_server = VcServer("0.0.0.0", 5001)
    while True:
        service_result = vc_server.start()
        vc_server.connection.sendall(__make_srp_protocol_header(service_result))
        vc_server.connection.send(read_as_binary(service_result.output_filepath))
        vc_server.connection.send(service_result.mime_type.encode())
