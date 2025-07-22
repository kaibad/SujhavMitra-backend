import mysql.connector
from flask import make_response
from configs.config import dbconfig

class user_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=dbconfig["host"],
                port=dbconfig["port"],
                user=dbconfig["username"],
                password=dbconfig["password"],
                database=dbconfig["database"],
            )
            self.conn.autocommit = True
            print("Connection established")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def all_user_model(self):
        if not self.conn:
            return {"error": "Database connection not established."}

        try:
            # it is better to create a cursor where or when we need beacase the persistent cursor (self.cursor) in __init__, which is not ideal and can cause Memory leaks. and Locked resources if not properly closed.
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sm_users")
            result = cursor.fetchall()
            cursor.close()

            if result:
                return make_response({"users": result}, 200)
            else:
                return make_response({"message": "No Data Found"}, 404)
        except Exception as e:
            return {"error": str(e)}