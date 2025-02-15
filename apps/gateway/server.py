import os, json

import gridfs, pika

from flask import Flask, request
from flask_pymongo import PyMongo

from auth import validate
from auth_service import access
from storage import util

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("queue"))
channel = connection.channel()

channel.exchange_declare(exchange="video", exchange_type="fanout")


@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if err:
        return err, 401

    return token

@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["is_admin"]:
        if len(request.files) != 1:
            return "exactly one file is required", 400

        if "file" not in request.files:
            return "no file", 400

        for _, file in request.files["file"]:
            err, status = util.upload(file, fs, channel, access)

            if err:
                return err, status

        return "success", 200

    return "not authorized", 403


# @app.route("/download", methods=["GET"])
# def download():
#     access, err = validate.token(request)

#     access = json.loads(access)

#     if access["is_admin"]:


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)