import pika, sys, os,  time
from send import email


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("queue"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = email.notification(body)

        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE_NAME"), 
        on_message_callback=callback
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

