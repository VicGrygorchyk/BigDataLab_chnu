"""Starts multiple workers"""
import sys
from functools import partial
from multiprocessing import Process

from influx_db_reader import InfluxDBReader
from mapper import map_data, map_to_worker
from reducer import reduce_data

MAX_WORKERS = 5


def start_workers():
    workers = [
        Process(
            target=partial(),
            args=()
        ) for _ in range(MAX_WORKERS)
    ]
    for process in workers:
        process.start()
    for process in workers:
        process.join()


if __name__ == "__main__":
    # get data from InfluxDB
    with InfluxDBReader() as reader:
        data = reader.read_data()
    values = []
    for records in data:
        for row in records:
            values.append(row.values)
    print(values[0])

    # map data
    mapped = map_data(values)
    # create workers and assign a reduce task for each

