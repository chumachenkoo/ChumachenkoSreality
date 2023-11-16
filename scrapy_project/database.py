import psycopg2
from psycopg2 import sql


class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table_name = 'flats'

    def create_database(self):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            conn.autocommit = True

            cur = conn.cursor()

            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.dbname)))

            cur.close()
            conn.close()

            print(f"Database {self.dbname} created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database {self.dbname} already exists.")
        except Exception as e:
            print("An error occurred:", e)

    def connect_to_db(self):
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

    def create_table_if_doesnt_exist(self):
        try:
            conn = self.connect_to_db()
            if conn:
                cur = conn.cursor()
                cur.execute(f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                tables = cur.fetchall()
                tables = [table[0] for table in tables]
                if self.table_name not in tables:
                    self.create_table(conn)
                cur.close()
                conn.close()
        except Exception as e:
            print("An error occurred:", e)

    def create_table(self, conn):
        try:
            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id serial PRIMARY KEY,
                    name VARCHAR(255),
                    image VARCHAR(255)
                );
            """)
            conn.commit()
            cur.close()
            print(f"Table {self.table_name} created successfully.")
        except Exception as e:
            print("An error occurred:", e)

    def insert_item(self, name, image):
        try:
            conn = self.connect_to_db()
            if conn:
                cur = conn.cursor()
                cur.execute(f"INSERT INTO {self.table_name} (name, image) VALUES (%s, %s)", (name, image))
                conn.commit()
                cur.close()
                conn.close()
                print(f"Item inserted successfully: {name}, {image}")
        except Exception as e:
            print("An error occurred:", e)

    def delete_all_items(self):
        try:
            conn = self.connect_to_db()
            if conn:
                cur = conn.cursor()
                cur.execute(f"DELETE FROM {self.table_name}")
                conn.commit()
                cur.close()
                conn.close()
                print("All items deleted successfully.")
        except Exception as e:
            print("An error occurred:", e)

    def load_all_items(self):
        try:
            conn = self.connect_to_db()
            if conn:
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM {self.table_name}")
                items = cur.fetchall()
                cur.close()
                conn.close()
                return items
        except Exception as e:
            print("An error occurred:", e)



def launch():
    db_manager = DatabaseManager(
        dbname="scrapy_db",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )

    db_manager.create_database()


if __name__ == "__main__":
    launch()

