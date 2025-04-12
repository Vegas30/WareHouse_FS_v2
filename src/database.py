import psycopg2
import logging

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="warehouse_db",
                user="postgres",
                password="7773",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
            logging.info("Database connection established successfully")
        except Exception as e:
            logging.error(f"Database connection error: {str(e)}")
            raise

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            self.conn.rollback()
            return False
            
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Database fetch error: {str(e)}")
            return []
            
    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Database fetch error: {str(e)}")
            return None 

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed") 