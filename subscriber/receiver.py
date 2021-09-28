import pika

QUEUE_NAME = 'log'


def listen_queue(callable):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        received_data = body.decode()
        print(f"Received {received_data}")
        callable(received_data)
        print("Done")

    channel.basic_consume(queue=QUEUE_NAME,
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()
    connection.close()
