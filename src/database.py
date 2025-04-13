import psycopg2
import logging
from PyQt6.QtWidgets import QMessageBox

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="warehouse_fs",
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

    def execute_query(self, query, params=None, parent_widget=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Exception as e:
            error_msg = f"Database error: {str(e)}"
            logging.error(error_msg)
            self.conn.rollback()
            
            # Отображаем сообщение об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при выполнении операции:\n{error_msg}"
                )
            return False
            
    def fetch_all(self, query, params=None, parent_widget=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            error_msg = f"Database fetch error: {str(e)}"
            logging.error(error_msg)
            
            # Отображаем сообщение об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при получении данных:\n{error_msg}"
                )
            return []
            
    def fetch_one(self, query, params=None, parent_widget=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Exception as e:
            error_msg = f"Database fetch error: {str(e)}"
            logging.error(error_msg)
            
            # Отображаем сообщение об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при получении данных:\n{error_msg}"
                )
            return None 

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed") 