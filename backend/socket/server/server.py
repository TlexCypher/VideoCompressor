import logging
import os.path
import socket


class TcpServer(object):
    """
    TcpServer
    This class is the server based tcp-connection.
    TcpServer is responsible for being video-compressor-server.
    This server only accepts mp4 file, if not denied to upload to itself.

    Protocol
        Header: 48bytes
            filesize: 32bytes
            filename_length: 16bytes

        Payload: Otherwise
    """

    def __init__(self, server_address: str, server_port: int) -> None:
        logging.basicConfig(level=logging.DEBUG, filename="vc-server.log", filemode='w')
        self.logger = logging.getLogger()

        self.server_address = server_address
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.server_address, self.server_port))
        self.logger.debug("Success to bind {}".format((self.server_address, self.server_port)))

        self.sock.listen(1)
        self.sock.settimeout(100)

        self.stream_rate = 1400
        self.filesize_length = 32
        self.filename_length = 8
        self.max_mp4_filesize = pow(2, self.filesize_length)
        self.header_length = self.filesize_length + self.filename_length

        self.dpath = "data"

        if not os.path.exists(self.dpath):
            os.makedirs(self.dpath)

    def _establish_connection(self):
        self.connection, self.client_address = self.sock.accept()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.logger.debug("Established a connection from {}".format(self.client_address))
        print("Success to establish connection with {}".format(self.client_address))

    def accept(self):
        try:
            while True:
                self._establish_connection()
                self.header = self.connection.recv(self.header_length)
                file_content_size = int.from_bytes(self.header[:self.filesize_length], "big")
                filename_size = int.from_bytes(self.header[self.filesize_length:], "big")
                print("File_size: {}, Filename_size: {}".format(file_content_size, filename_size))

                self.filename = self.connection.recv(filename_size).decode('utf-8')
                print("Filename: {}".format((os.path.abspath(self.dpath) + "/" + self.filename)))

                with open(os.path.abspath(self.dpath) + "/" + self.filename, "wb+") as f:
                    data = self.connection.recv(self.stream_rate)
                    while data:
                        f.write(data)
                        data = self.connection.recv(self.stream_rate)
                    print("End to write into {}".format(os.path.abspath(self.dpath) + "/" + self.filename))
                    self.logger.info("Success to write into {}".format(os.path.abspath(self.dpath) + "/" + self.filename))

        except TimeoutError:
            print("No data from client.\nClosing connection.")
            self.sock.close()


if __name__ == '__main__':
    server = TcpServer("0.0.0.0", 5001)
    server.accept()
