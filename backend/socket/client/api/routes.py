from config import app
from flask import request, jsonify


@app.route("/compress", methods=["POST"])
def compress_video():
    byteFileContent = request.json["content"]
    filename = request.json["name"]

    with open("../../server/raw/" + filename, "wb+") as f:
        f.write(bytes(byteFileContent))
    return jsonify({"message": "success to compress"})


if __name__ == '__main__':
    app.run(debug=True)
