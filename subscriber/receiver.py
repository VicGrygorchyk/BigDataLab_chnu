from typing import TYPE_CHECKING

import pika

if TYPE_CHECKING:
    from subscriber.db_connector import DBConnector


QUEUE_NAME = 'log'


def listen_queue(connector: 'DBConnector'):
    """Listen for a new message in MQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        def callback(ch, method, properties, body):
            received_data = body.decode()
            print(f"Received {received_data}")
            # save data to DB
            connector.write_data(received_data)
            print("Done")

        channel.basic_consume(queue=QUEUE_NAME,
                              auto_ack=True,
                              on_message_callback=callback)
        channel.start_consuming()
    finally:
        connection.close()
