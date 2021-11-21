from pyspark.sql import SparkSession, DataFrame

from postgres_connector import db_properties, url, database


class PySparkManager:

    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Python Spark Lab 2") \
            .config("spark.jars", "/home/mudro/Documents/Hryhorchuk_BigData_Lab1/postgresql-42.3.1.jar") \
            .getOrCreate()

    def read_data_frames(self, values) -> DataFrame:
        data_frame = self.spark.createDataFrame(values)
        return data_frame

    def write_data_frames_to_db(self, data_frames: DataFrame):
        data_frames.write.jdbc(url=url, table=f'{database}.logs', mode='overwrite', properties=db_properties)

