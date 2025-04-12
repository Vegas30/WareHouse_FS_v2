import psycopg2
from PyQt6.QtWidgets import QMessageBox
import logging
from database import Database


class AuthService:
    @staticmethod
    def authenticate(username: str, password: str) -> tuple:
        """
        Authentication method (simplified, without hashing)
        Returns: (success: bool, full_name: str, is_admin: bool)
        """
        try:
            db = Database()
            db.cursor.execute(
                "SELECT password_hash, full_name, is_admin FROM users WHERE username = %s",
                (username,)
            )
            result = db.cursor.fetchone()

            if result:
                db_password, full_name, is_admin = result
                if password == db_password:  # In production, should use password hashing
                    return True, full_name, is_admin

            return False, "", False
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return False, "", False

    @staticmethod
    def change_password(username: str, current_password: str, new_password: str) -> bool:
        """Changes user password (simplified, without hashing)"""
        try:
            db = Database()
            
            # Verify current password
            db.cursor.execute(
                "SELECT 1 FROM users WHERE username = %s AND password_hash = %s",
                (username, current_password)
            )
            if not db.cursor.fetchone():
                return False

            # Update password
            return db.execute_query(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (new_password, username)
            )
        except Exception as e:
            logging.error(f"Password change error: {str(e)}")
            return False

    def get_user_by_id(self, user_id):
        """
        Retrieves user information by user ID
        """
        try:
            query = """
                SELECT user_id, username, full_name, is_admin, email
                FROM users
                WHERE user_id = %s
            """
            result = self.db.fetch_one(query, (user_id,))
            
            if result:
                user_id, username, full_name, is_admin, email = result
                return {
                    "user_id": user_id,
                    "username": username,
                    "full_name": full_name,
                    "is_admin": is_admin,
                    "email": email
                }
            return None
            
        except Exception as e:
            logging.error(f"User retrieval error: {str(e)}")
            return None
    
    def is_admin(self, user_id):
        """
        Checks if a user has admin privileges
        """
        user = self.get_user_by_id(user_id)
        return user and user["is_admin"] 