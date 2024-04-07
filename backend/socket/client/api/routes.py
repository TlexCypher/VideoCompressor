import enum
import logging
import os.path

from config import app
from compress.serviceResult import ServiceResult2
from logic.vc_client import VcClient
from flask import request, jsonify


@app.route("/service", methods=["POST"])
def run_service():
    class _ServiceResultCode(enum.Enum):
        SUCCESS = 0
        FAIL = 1

    logging.basicConfig(level=logging.DEBUG, filemode='w', filename="routes.log")
    logger = logging.getLogger()

    byteFileContent = bytes(request.json["content"])
    filename = request.json["name"]
    save_raw_data(byteFileContent, filename)
    _service_result = run_vc_client(request.json, filename)

    if _service_result.return_code == _ServiceResultCode.SUCCESS.value:
        logger.info("Success to end service.")
        return jsonify({"message": "success to end service."})

    else:
        logger.info("Failed to end service.")
        return jsonify({"message": "failed to end service."})


def save_raw_data(byteFileContent: bytes, filename: str):
    raw_data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                      "server/raw")
    if not os.path.exists(raw_data_directory):
        os.makedirs(raw_data_directory)
    raw_video_filepath = os.path.join(raw_data_directory, filename)
    with open(raw_video_filepath, "wb+") as f:
        f.write(byteFileContent)


def run_vc_client(request_json: dict, payload_filename: str) -> ServiceResult2:
    vc_client = VcClient("0.0.0.0", 5001, payload_filename)
    vc_client.upload()
    _service_result = vc_client.compress_service_start(request_json)
    return _service_result


if __name__ == '__main__':
    app.run(debug=True)
