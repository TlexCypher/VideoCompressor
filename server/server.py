import socket
import json
import os
import subprocess


class Server:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.read_size = 1400

    def start(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        connection, _ = self.socket.accept()

        try:
            while True:
                connection.send("Start the Video Compressor Service.".encode("utf-8"))
                data = connection.recv(self.read_size)
                data_json = json.loads(data)
                filename = data_json["filename"]
                filename_length = data_json["filename_length"]
                filesize = data_json["filesize"]
                print(
                    "filename:{}, filename_length: {}, filesize: {}",
                    filename,
                    filename_length,
                    filesize,
                )

                if filesize == 0:
                    print("No data from the client.")

                with open(os.path.join(filename), "wb+") as f:
                    while filesize > 0:
                        data = connection.recv(
                            filesize if filesize < self.read_size else self.read_size
                        )
                        f.write(data)
                        filesize -= self.read_size

                connection.send("Upload finish".encode("utf-8"))

                while True:
                    cmd = connection.recv(1024).decode("utf-8")
                    subprocess.run(cmd.split(" "))
                    connection.send("File generated\n".encode("utf-8"))

                    continue_question = connection.recv(1024).decode("utf-8")

                    if continue_question == "0":
                        os.remove(filename)
                        connection.send("End the service".encode("utf-8"))
        except Exception as e:
            print("Error" + str(e))

        finally:
            print("Closing connection.")
            connection.close()


if __name__ == "__main__":
    server = Server("", 9000)
    server.start()
