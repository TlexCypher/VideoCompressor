import socket
import json


class Client:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREM)
        self.address = address
        self.port = port
        self.read_size = 1400

    def start(self):
        while True:
            self.socket.bind((self.address, self.port))
            self.socket.listen(1)

            connection, _ = self.socket.accept()
            connection.send("Start the Video Compressor Service.".encode("utf-8"))
            data = connection.recv(self.read_size)
            data_json = json.loads(data)
            filename = data_json["filename"]
            filename_length = data_json["filename_length"]
            filesize = data_json["filesize"]
            print("filename:{}, filename_length: {}, filesize: {}")

            if filesize == 0:
                print("No data from the client.")
