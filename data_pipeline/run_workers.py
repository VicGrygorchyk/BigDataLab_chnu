"""Starts multiple workers"""
import sys

from influx_db_reader import InfluxDBReader


if __name__ == "__main__":
    # get data from InfluxDB
    with InfluxDBReader() as reader:
        data = reader.read_data()
    for records in data:
        for row in records:
            print(row.values)
