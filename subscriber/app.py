import sys

from receiver import listen_queue
from db_connector import publish_to_db


if __name__ == "__main__":
    try:
        listen_queue(publish_to_db)
    except KeyboardInterrupt:
        print('Exiting listener app.')
        sys.exit(0)
