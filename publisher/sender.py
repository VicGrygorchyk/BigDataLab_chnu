import pika


QUEUE_NAME = 'log'


def send_msg(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=data)
    print(f" [x] Sent {data}")

    connection.close()
