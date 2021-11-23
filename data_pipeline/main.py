"""Calculate data with pyspark multiple workers"""
from influx_db_reader import InfluxDBReader
from spark_manager import PySparkManager
from postgres_connector import PostgresConnector

MAX_WORKERS = 5


if __name__ == "__main__":
    # get data from InfluxDB
    with InfluxDBReader() as reader:
        data = reader.read_data()
    # write data to list
    values = []
    for records in data:
        for row in records:
            values.append(row.values)
    # connect to Postgres
    with PostgresConnector() as connector:
        # get average
        connector.create_db()
        manager = PySparkManager()
        spark = manager.spark
        print('-----------------------')
        agg_result = manager.get_payment_avg(data=values, workers_amount=MAX_WORKERS)
        result = agg_result.collect()
        # save to DB
        connector.write_data(result)
