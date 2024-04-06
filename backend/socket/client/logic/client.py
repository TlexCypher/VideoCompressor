import logging
import os.path
import socket
import sys


class TcpClient(object):
    """
    Protocol
        Header: 48bytes
            filesize: 32bytes
            filename: 16bytes

        Payload: Otherwise
    """

    def __init__(self, server_address, server_port):
        logging.basicConfig(level=logging.DEBUG, filename="vc-client.log", filemode='w')
        self.logger = logging.getLogger()

        self.server_address = server_address
        self.server_port = server_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Success to make a socket.")

        self.stream_rate = 1400
        self.header_size = 64

    def _connect_with_server(self):
        try:
            print("Server_address:", self.server_address)
            print("Server_port:", self.server_port)

            self.sock.connect((self.server_address, self.server_port))
        except socket.error as err:
            print("Failed to connect with server.")
            print(err)
            self.logger.error("Failed to connect with server.")
            sys.exit(1)

    def upload(self):
        self._connect_with_server()
        self._get_user_input()
        try:
            with open(self.filepath, "rb+") as f:
                self.__send_header()
                self.sock.send(os.path.basename(f.name).encode('utf-8'))

                data_length = self.filesize
                data = f.read(data_length if data_length < self.stream_rate else self.stream_rate)

                while data:
                    self.sock.send(data)
                    data_length -= len(data)
                    data = f.read(data_length if data_length < self.stream_rate else self.stream_rate)
                print("Success to upload!")
                self.logger.info("Success to upload!")

        finally:
            print("Close connection.")
            self.logger.info("Close connection")
            self.sock.close()

    def _get_user_input(self):
        self.filepath = input("Please enter absolute filepath: ")
        if not os.path.exists(self.filepath):
            self.logger.error("No such file: {}".format(self.filepath))
            raise Exception("No such file. Failed to upload.")

    def __send_header(self):
        print(self.__make_protocol_header())
        self.sock.send(self.__make_protocol_header())

    def __make_protocol_header(self) -> bytes:
        with open(self.filepath, "rb+") as f:
            return self._get_filesize(f).to_bytes(32, "big") + len(os.path.basename(f.name)).to_bytes(8, "big")

    def _get_filesize(self, file) -> int:
        file.seek(0, os.SEEK_END)
        self.filesize = file.tell()
        file.seek(0, 0)
        print("File size from seek: {}".format(self.filesize))
        print("File name from client: {}".format(file.name))
        return self.filesize


if __name__ == '__main__':
    client = TcpClient("0.0.0.0", 5001)
    client.upload()
