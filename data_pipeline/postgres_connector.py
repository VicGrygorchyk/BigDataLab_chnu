"""Writes data to Postgres DB"""
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
        self.conn = psycopg2.connect(f'user={user} password={password} host={host}')
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return self

    def create_db(self):
        """ Connect to the PostgreSQL database server """
        conn = self.conn
        try:
            # create a cursor
            cur = conn.cursor()
            # create DB
            cur.execute(sql.SQL(f"CREATE DATABASE {database};"))
            # write data
            # commit the changes to the database
            conn.commit()
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def write_data(self):
        # create a cursor
        cur = self.conn.cursor()
        # create DB
        cur.execute(sql.SQL(
            f"CREATE TABLE IF NOT EXISTS {table_name} ("
            "ID INT PRIMARY KEY NOT NULL,"
            "DATE DATE NOT NULL DEFAULT CURRENT_DATE,"
            "COUNTRY CHAR(10),"
            "CITY CHR(10),"
            "CLICK_COST FLOAT(10)"
            ");"))
        self.conn.commit()
        # TODO
        cur.execute(sql.SQL(
            f"INSERT INTO {table_name} "
        ))
        self.conn.commit()
        cur.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
