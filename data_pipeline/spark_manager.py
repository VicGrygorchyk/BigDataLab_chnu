from typing import List

from pyspark.context import SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions


class PySparkManager:

    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Python Spark Lab 2") \
            .config("spark.jars", "/home/mudro/Documents/Hryhorchuk_BigData_Lab1/postgresql-42.3.1.jar") \
            .getOrCreate()

    def read_data_frames(self, values) -> DataFrame:
        data_frame = self.spark.createDataFrame(values)
        return data_frame

    def get_payment_avg(self, data: List, workers_amount) -> DataFrame:
        df = self.get_context().parallelize(data, workers_amount).toDF()
        result = df.filter(df['payment'].isNotNull()) \
            .groupBy(df['country'], df['city']) \
            .agg(functions.mean(df['payment']))
        result.show()
        return result

    def get_context(self) -> SparkContext:
        return self.spark.sparkContext
