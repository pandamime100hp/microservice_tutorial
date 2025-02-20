import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy


def start(body, fs_videos, fs_mp3s, channel):
    message: dict = json.loads(body)
    file_id: str = message["file_id"]

    tf = tempfile.NamedTemporaryFile()

    out = fs_videos.get(ObjectId(file_id))

    tf.write(out.read())

    audio = moviepy.VideoFileClip(tf.name).audio

    tf.close()

    tf_path = f"{tempfile.gettempdir()}/{file_id}.mp3"

    audio.write_audiofile(tf_path)

    f = open(tf_path, "rb")
    data = f.read()
    mp3_id = fs_mp3s.put(data)
    f.close()

    os.remove(tf_path)

    message["mp3_id"] = str(mp3_id)

    try:
        channel.basic_publish(
            exchange="", 
            routing_key=os.environ.get("MP3_QUEUE_NAME"), 
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs_mp3s.delete(mp3_id)
        return "failed to publish to mp3 queue"
    
    return "success"