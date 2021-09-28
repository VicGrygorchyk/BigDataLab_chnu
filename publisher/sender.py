import pika


QUEUE_NAME = 'log'


def send_msg(data):
    """Send message to Broker."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=data)
        print(f"Sent {data}")
    finally:
        connection.close()
