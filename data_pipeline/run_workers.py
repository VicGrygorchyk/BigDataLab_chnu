"""Starts multiple workers"""
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
    PostgresConnector().create_db()
    manager = PySparkManager()
    spark = manager.spark
    data_frame = manager.read_data_frames(values)
    print('-----------------------')
    print(data_frame)
    manager.write_data_frames_to_db(data_frame)
