"""Starts multiple workers"""
from pyspark.sql import functions

from influx_db_reader import InfluxDBReader
from spark_manager import PySparkManager
from postgres_connector import PostgresConnector

MAX_WORKERS = 5


if __name__ == "__main__":
    # get data from InfluxDB
    with InfluxDBReader() as reader:
        data = reader.read_data()
    values = []
    for records in data:
        for row in records:
            values.append(row.values)
    with PostgresConnector() as connector:
        connector.create_db()
        manager = PySparkManager()
        spark = manager.spark
        print('-----------------------')
        data_frame = manager.read_data_frames(values)
        # reduce to show mean payment for each city
        data_frame.filter(data_frame['payment'].isNotNull()) \
            .select(data_frame['country'], data_frame['city'], data_frame['payment']) \
            .groupBy(data_frame['country'], data_frame['city']) \
            .agg(functions.mean(data_frame['payment'])) \
            .show()

    # manager.write_data_frames_to_db(data_frame)
