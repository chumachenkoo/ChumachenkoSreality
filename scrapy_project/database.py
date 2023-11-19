import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


load_dotenv()


class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table_name = 'flats'

    def _connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            print("An error occurred while connecting to the database:", e)

    def __enter__(self):
        self.conn = self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def create_database(self):
        try:
            with self._connect() as conn:
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
                print(f"Database {self.dbname} created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database {self.dbname} already exists.")
        except Exception as e:
            print("An error occurred:", e)

    def create_table_if_doesnt_exist(self):
        try:
            with self._connect() as conn:
                if conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                    tables = cur.fetchall()
                    tables = [table[0] for table in tables]
                    if self.table_name not in tables:
                        self.create_table(conn)
        except Exception as e:
            print("An error occurred:", e)

    def create_table(self, conn):
        try:
            if conn:
                cur = conn.cursor()
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id serial PRIMARY KEY,
                        name VARCHAR(255),
                        image VARCHAR(255)
                    );
                """)
                conn.commit()
                print(f"Table {self.table_name} created successfully.")
        except Exception as e:
            print("An error occurred:", e)

    def insert_item(self, name, image):
        try:
            with self._connect() as conn:
                if conn:
                    cur = conn.cursor()
                    cur.execute(f"INSERT INTO {self.table_name} (name, image) VALUES (%s, %s)", (name, image))
                    conn.commit()
                    print(f"Item inserted successfully: {name}, {image}")
        except Exception as e:
            print("An error occurred:", e)

    def delete_all_items(self):
        try:
            with self._connect() as conn:
                if conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM {self.table_name}")
                    conn.commit()
                    print("All items deleted successfully.")
        except Exception as e:
            print("An error occurred:", e)

    def load_all_items(self):
        try:
            with self._connect() as conn:
                if conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM {self.table_name}")
                    items = cur.fetchall()
                    return items
        except Exception as e:
            print("An error occurred:", e)


db_manager = DatabaseManager(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
)
