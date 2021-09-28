import time

import pika

QUEUE_NAME = 'log'


def listen_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")

    channel.basic_consume(queue=QUEUE_NAME,
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()
    connection.close()
