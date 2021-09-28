import sys

from receiver import listen_queue
from db_connector import DBConnector


if __name__ == "__main__":
    try:
        with DBConnector() as connector:
            listen_queue(connector)
    except KeyboardInterrupt:
        print('Exiting listener app.')
        sys.exit(0)
