import pika, json


def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as e:
        return "internal server error", 500
    
    message = {
        "file_id": file_id, 
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
    except:
        fs.delete(file_id)
        return "internal server error", 500
    
    return None, 201