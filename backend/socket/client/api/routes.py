import os.path

from config import app
from logic.vc_client import VcClient
from flask import request, jsonify

from typing import Any


@app.route("/service", methods=["POST"])
def run_service():
    byteFileContent = bytes(request.json["content"])
    filename = request.json["name"]
    save_raw_data(byteFileContent, filename)
    run_vc_client(request.json, filename)
    return jsonify({"message": "success to compress"})


def save_raw_data(byteFileContent: bytes, filename: str):
    raw_data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                      "server/raw")
    if not os.path.exists(raw_data_directory):
        os.makedirs(raw_data_directory)
    raw_video_filepath = os.path.join(raw_data_directory, filename)
    print("raw video filepath>>", raw_video_filepath)
    with open(raw_video_filepath, "wb+") as f:
        f.write(byteFileContent)


def run_vc_client(request_json: dict, payload_filename: str):
    vc_client = VcClient("0.0.0.0", 5001, payload_filename)
    vc_client.upload()
    vc_client.compress_service_start(request_json)


if __name__ == '__main__':
    app.run(debug=True)
