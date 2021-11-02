"""Starts multiple workers"""
import sys

from influx_db_reader import DBConnector


if __name__ == "__main__":
    try:
        with DBConnector() as connector:
            connector.read_data()
    except KeyboardInterrupt:
        print('Exiting listener app.')
        sys.exit(0)
