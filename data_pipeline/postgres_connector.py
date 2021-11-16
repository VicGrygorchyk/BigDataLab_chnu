"""Writes data to Postgres DB"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


host = "localhost",
database = "test_database",
user = "postgres",
password = "mapreduce"
url = f'jdbc:postgresql://localhost:5432/{database}'
db_properties = {'username': user, 'password': password, 'url': url, 'driver': 'org.postgresql.Driver'}


class PostgresConnector:

    def __init__(self):
        self.host = host,
        self.database = database,
        self.user = user,
        self.password = password

    def create_db(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # create a cursor
            cur = conn.cursor()
            # create DB
            cur.execute(sql.SQL(f"CREATE DATABASE {sql.Identifier(self.database)}"))
            # write data
            # commit the changes to the database
            conn.commit()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
