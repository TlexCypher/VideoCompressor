import os
import socket
import json


class Client:
    def __init__(self, address, server_port) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.server_port = server_port
        self.max_size = pow(2, 32)
        self.read_size = 1400
        self.extension = "mp4"

    def start(self):
        try:
            self.socket.connect((self.address, self.server_port))
        except socket.error as err:
            print(err)
            exit(1)

    def upload(self):
        print(self.socket.recv(self.read_size).decode('utf-8'))
        self.filepath = input("Input filename wanna to compress: ")
        filename = os.path.basename(self.filepath)
        extension = filename[-len(self.extension) :]

        with open(self.filepath, "rb") as f:
            filesize = os.path.getsize(self.filepath)

            if filesize > self.max_size:
                raise Exception("Your file is too large, under 4GB.")

            if extension != self.extension:
                raise Exception("Only mp4 file is acceptable.")

            data_json = {
                'filename' : filename,
                'filename_length': len(filename),
                'filesize': filesize
            }

            self.socket.send(json.dumps(data_json).encode('utf-8'))
            data = f.read(self.read_size)

            while data:
                self.socket.send(data)
                data = f.read(self.read_size)

            print("Server response: ", self.socket.recv(16).decode("utf-8"))

            while True:

