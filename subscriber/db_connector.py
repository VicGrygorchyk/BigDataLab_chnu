from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

BUCKET_NAME = 'log_bucket'


class DBConnector:

    def __init__(self):
        self.client = None
        self.write_api = None

    def __enter__(self):
        self.client = InfluxDBClient(url="http://influxdb:8086", username="admin", password="adminpass",
                                     ssl=False, verify_ssl=False, token="admintoken", org="chnu")

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        return self

    def write_data(self, data):
        """Write data to the bucket.
        Data should have such values as: id, userid, country, city, campaign, payment
        """
        received = data.split(',')

        try:
            p = Point("log_line") \
                .field("id", received[0]) \
                .tag("userid", received[1]) \
                .tag("country", received[2]) \
                .tag("city", received[3]) \
                .tag("campaign", received[4]) \
                .tag("payment", received[-1])
        except IndexError:
            raise Exception('Error: incorrect data length. '
                            'Make sure there are such values as: id, userid, country, city, campaign, payment')

        self.write_api.write(bucket=BUCKET_NAME, record=p)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing connection to DB.')
        self.client.close()
