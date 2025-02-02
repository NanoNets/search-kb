import os
import psycopg2
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id SERIAL PRIMARY KEY,
                type TEXT,
                embedding BYTEA,
                resource_id TEXT,
                time_stamp TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_record(self, record):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO knowledge (type, embedding, resource_id, time_stamp)
            VALUES (%s, %s, %s, %s)
        ''', record)
        self.conn.commit()
