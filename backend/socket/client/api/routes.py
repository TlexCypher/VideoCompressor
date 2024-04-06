from config import app
from flask import request, jsonify


@app.route("/service", methods=["POST"])
def run_service():
    byteFileContent = bytes(request.json["content"])
    filename = request.json["name"]
    service = request.json["service"]
    save_raw_data(byteFileContent, filename)

    # TODO: call server's api.
    # if service == "Compress":
    
    return jsonify({"message": "success to compress"})


def save_raw_data(byteFileContent: bytes, filename: str):
    with open("../../server/raw/" + filename, "wb+") as f:
        f.write(byteFileContent)


if __name__ == '__main__':
    app.run(debug=True)
