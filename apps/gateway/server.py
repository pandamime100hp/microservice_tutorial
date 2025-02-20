import os, json

from bson import ObjectId
import gridfs, pika

from flask import Flask, request, send_file
from flask_pymongo import PyMongo

from auth import validate
from auth_service import access
from storage import util

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")

videos_client = PyMongo(app, uri=f"{mongo_uri}/videos")
mp3s_client = PyMongo(app, uri=f"{mongo_uri}/mp3s")

video_fs = gridfs.GridFS(videos_client.db)
mp3_fs = gridfs.GridFS(mp3s_client.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("queue"))
channel = connection.channel()

channel.exchange_declare(exchange="videos", exchange_type="fanout")


@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if err:
        return err, 401

    return token


@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err, 401

    access = json.loads(access)

    if access["is_admin"]:
        if len(request.files) != 1:
            return "exactly one file is required", 400

        if "file" not in request.files:
            return "no file", 400

        for _, file in request.files.items():
            err, status = util.upload(file, video_fs, channel, access)

            if err:
                return err, status

        return "success", 200

    return "not authorized", 401


@app.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err, 401

    access = json.loads(access)

    if access["is_admin"]:
        file_id = request.args.get("file_id")

        if not file_id:
            return "missing file_id", 400

        # err, status = util.download(file_id, mp3_fs, channel, access)

        # if err:
        #     return err, status

        try:
            out = mp3_fs.get(ObjectId(file_id)).read()
            return send_file(out, download_name=f"{file_id}.mp3"), 200
        except Exception as e:
            return f"internal server error: {e}", 500
    
    return "not authorized", 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)