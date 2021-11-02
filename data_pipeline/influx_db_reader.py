"""Connects to influx db and reads data from."""
from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxRecord

BUCKET_NAME = 'log_bucket'


class DBConnector:

    def __init__(self):
        self.client = None
        self.write_api = None
        self.query_api = None

    def __enter__(self):
        self.client = InfluxDBClient(url="http://localhost:8086", username="admin", password="adminpass",
                                     ssl=False, verify_ssl=False, token="admintoken", org="chnu")
        self.query_api = self.client.query_api()
        return self

    def read_data(self):
        tables = self.query_api.query(f'from(bucket:"{BUCKET_NAME}") |> range(start: -10m)')

        for table in tables:
            print(f"Table is {table}")
            for row in table.records:  # type: FluxRecord
                print(f"\nRow is: {row.values}.")
                print("----" * 20)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing connection to DB.')
        self.client.close()
