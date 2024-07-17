import psycopg2
from psycopg2 import sql
import os
from psycopg2.extras import execute_batch
from ..config import logger, Environment
from .constants import Query

env = Environment()

class Datalake:
    def __init__(self) -> None:
        self.host = env.get_value("POSTGRES_DATALAKE_HOST")
        self.dbname = env.get_value("POSTGRES_DATALAKE_DBNAME")
        self.user = env.get_value("POSTGRES_DATALAKE_USER")
        self.password = env.get_value("POSTGRES_DATALAKE_PASS")
        self.port = env.get_value("POSTGRES_DATALAKE_PORT")
        
        logger.info(f"Xo ve essas creds.. {self.host} - {self.dbname} - {self.user} - {self.password} - {self.port}")
        self.conn = self.connect()
    
    def connect(self):
        try:
            return psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
        except Exception as e:
            raise ValueError(f"Error: {self.host} ")
        
    def insert_data(self, insert_query_name, data):
        try:
            logger.info(f"Inserting {len(data)} rows into {insert_query_name}...")

            cursor = self.conn.cursor()

            execute_batch(cursor, vars(Query)[insert_query_name], data)
            
            self.conn.commit()
            
            cursor.close()
        except Exception as e:
            raise e        
            

        
        
        