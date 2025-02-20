import pika, json


def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as e:
        return f"fs: internal server error: {e}", 500
    
    message = {
        "file_id": str(file_id), 
        "mp3_id": None, 
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="", 
            routing_key="video", 
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs.delete(file_id)
        return f"channel: internal server error: {e}", 500
    
    return None, 201


def download(file_id, fs, channel, access):
    