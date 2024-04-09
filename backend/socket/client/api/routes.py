import base64
import enum
import logging
import os.path
from http import HTTPStatus

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
        # write video content
        saved_filepath = save_service_result(_service_result, filename)
        return jsonify({
            "status": HTTPStatus.OK,
            "content": base64.b64encode(read_as_binary(saved_filepath)).decode('utf-8')
        })

    else:
        logger.info("Failed to end service.")
        return jsonify({
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "content": None
        })


def save_raw_data(byteFileContent: bytes, filename: str) -> None:
    raw_data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw")
    if not os.path.exists(raw_data_directory):
        os.makedirs(raw_data_directory)
    raw_video_filepath = os.path.join(raw_data_directory, filename)
    _save(byteFileContent, raw_video_filepath)


def save_service_result(_service_result: ServiceResult2, filename: str) -> str:
    service_result_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "result")
    if not os.path.exists(service_result_directory):
        os.makedirs(service_result_directory)
    service_result_video_filepath = os.path.join(service_result_directory, "processed_" + filename)
    _save(_service_result.file_content, service_result_video_filepath)
    return service_result_video_filepath


def _save(content: bytes, abs_filepath: str):
    with open(abs_filepath, "wb+") as f:
        f.write(content)


def run_vc_client(request_json: dict, payload_filename: str) -> ServiceResult2:
    vc_client = VcClient("0.0.0.0", 5001, payload_filename)
    vc_client.upload()
    _service_result = vc_client.compress_service_start(request_json)
    return _service_result


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
            current_chunk = f.read(file_size if file_size < stream_rate else stream_rate)
            data += current_chunk
            file_size -= len(current_chunk)

        return data


if __name__ == '__main__':
    app.run(debug=True)
