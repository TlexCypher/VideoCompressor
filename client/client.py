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
            self.upload()

        except socket.error as err:
            print(err)
            exit(1)

    def upload(self):
        try:
            print(self.socket.recv(self.read_size).decode("utf-8"))
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
                    "filename": filename,
                    "filename_length": len(filename),
                    "filesize": filesize,
                }

                self.socket.send(json.dumps(data_json).encode("utf-8"))
                data = f.read(self.read_size)

                while data:
                    self.socket.send(data)
                    data = f.read(self.read_size)

                print("Server response: ", self.socket.recv(16).decode("utf-8"))

                while True:
                    cmd = ""
                    height = ""
                    width = ""
                    start = ""
                    end = ""
                    flamerate = ""
                    resize = ""

                    select_mode = input(
                        "Please enter a number from 0 to 4\n"
                        + "0 : 動画ファイルを圧縮する\n"
                        + "1 : 動画の解像度を変更する\n"
                        + "2 : 動画の縦横比を変更する\n"
                        + "3 : 動画をオーディオに変換する\n"
                        + "4 : 時間範囲からGIFを作成する\n"
                    )

                    if select_mode == "0":
                        select_level = input(
                            "Please select the degree of compression\n"
                            + "0 : low\n"
                            + "1 : medium\n"
                            + "2 : high\n"
                        )
                        if select_level == "0":
                            cmd = (
                                "ffmpeg -i "
                                + filename
                                + " -c:v libx264 output/output_low.mp4"
                            )
                        elif select_level == "1":
                            cmd = (
                                "ffmpeg -i "
                                + filename
                                + " -c:v libx265 output/output_medium.mp4"
                            )
                        elif select_level == "2":
                            cmd = (
                                "ffmpeg -i "
                                + filename
                                + " -c:v libx265 -b:v 500k output/output_high.mp4"
                            )

                    elif select_mode == "1":
                        height = input("Please enter the height (ex. 1280) : ")
                        width = input("Please enter the width (ex. 720) : ")
                        cmd = (
                            "ffmpeg -i "
                            + filename
                            + " -filter:v scale="
                            + height
                            + ":"
                            + width
                            + " -c:a copy output/output_scale.mp4"
                        )

                    elif select_mode == "2":
                        height = input("Please enter the height (ex. 16) : ")
                        width = input("Please enter the width (ex. 9) : ")
                        cmd = (
                            "ffmpeg -i "
                            + filename
                            + " -pix_fmt yuv420p -aspect "
                            + height
                            + ":"
                            + width
                            + " output/output_aspect.mp4"
                        )

                    elif select_mode == "3":
                        cmd = "ffmpeg -i " + filename + " -vn output/output_audio.mp3"

                    elif select_mode == "4":
                        start = input("Input start position (ex. 00:00:20) : ")
                        end = input("Input end position (ex. 10) : ")
                        flamerate = input("Input flame rate (ex. 10) : ")
                        resize = input("Input resize (ex. 300) : ")
                        cmd = (
                            "ffmpeg -ss "
                            + start
                            + " -i "
                            + filename
                            + " -to "
                            + end
                            + " -r "
                            + flamerate
                            + " -vf scale="
                            + resize
                            + ":-1 output/output_gif.gif"
                        )

                    self.socket.send(cmd.encode("utf-8"))

                    print(self.socket.recv(1024).decode("utf-8"))

                    continue_question = input(
                        "Do you want to continue ?\n" + "0 : No\n" + "1 : Yes\n"
                    )
                    self.socket.send(continue_question.encode("utf-8"))

                    if continue_question == "0":
                        print(self.socket.recv(1024).decode("utf-8"))
                        break
        finally:
            print("Closing socket")
            self.socket.close()


if __name__ == "__main__":
    client = Client("", 9000)
    client.start()
