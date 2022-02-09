"""Writes data to Postgres DB"""
import datetime

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


host = "localhost"
database = "test_database"
user = "postgres"
password = "mapreduce"
url = f'jdbc:postgresql://localhost:5432/{database}'
db_properties = {'username': user, 'password': password, 'url': url, 'driver': 'org.postgresql.Driver'}
table_name = 'clicks_cost'


class PostgresConnector:

    def __init__(self):
        self.conn = None

    def __enter__(self):
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        self.conn = psycopg2.connect(f'user={user} password={password} host={host} dbname={database}')
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return self

    def get_data(self, date_from, date_to):
        # create a cursor
        cur = self.conn.cursor()
        cur.execute(sql.SQL(
            f"SELECT (date,country,city,click_cost) FROM {table_name} "
            f"WHERE date >= '{date_from}' AND date <= '{date_to}';"
        ))
        data = cur.fetchall()
        self.conn.commit()
        cur.close()
        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')