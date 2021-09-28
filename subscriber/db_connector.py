from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.flux_table import FluxRecord
from influxdb_client.client.write_api import SYNCHRONOUS

BUCKET_NAME = 'log_bucket'


def publish_to_db(data):
    client = InfluxDBClient(url="http://localhost:8086", username="admin", password="adminpass",
                            ssl=False, verify_ssl=False, token="admintoken", org="chnu")

    received = data.split(',')
    # should have such values as: id, userid, country, city, campaign, payment

    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    p = Point("log_line") \
        .field("id", received[0]) \
        .tag("userid", received[1]) \
        .tag("country", received[2]) \
        .tag("city", received[3]) \
        .tag("campaign", received[4]) \
        .tag("payment", received[-1])

    write_api.write(bucket=BUCKET_NAME, record=p)

    # using Table structure
    tables = query_api.query(f'from(bucket:"{BUCKET_NAME}") |> range(start: -10m)')

    for table in tables:
        print(f"Table is {table}")
        for row in table.records:  # type: FluxRecord
            print(f"\nRow is: {row.values}.")
            print("----" * 50)
