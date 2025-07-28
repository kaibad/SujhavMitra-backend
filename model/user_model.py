import mysql.connector
from flask import make_response
from configs.config import dbconfig,JWT_SECRET
from datetime import datetime,timedelta
import jwt

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

    # user Get Model: this is for the admin to manage users through dashboard
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

    # user SignUp Model 
    def signup_user_model(self, user_data):
        if not self.conn:
            return {"error": "Database connection not established."}
        try:
            cursor = self.conn.cursor()
            user_role_id = 3  # hardcoded role_id for "user"
            
            query = "INSERT INTO sm_users (name, phone, email, role_id, password) VALUES (%s, %s, %s, %s, %s)"
            values = (
                user_data["name"],
                user_data["phone"],
                user_data["email"],
                3, 
                user_data["password"]
            )
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
            return make_response({"message": "User signed up successfully."}, 201)
        except Exception as e:
            return {"error": str(e)}

    
    # user Update Model
    def update_user_model(self, user_data):
        if not self.conn:
            return {"error": "Database connection not established."}

        if 'id' not in user_data:
            return make_response({"error": "User ID is required for update."}, 400)

        try:
            cursor = self.conn.cursor()
            user_id = user_data['id']

            fields = []
            values = []

            for key, value in user_data.items():
                if key != "id":
                    fields.append(f"{key} = %s")
                    values.append(value)

            if not fields:
                cursor.close()
                return make_response({"message": "Nothing to update."}, 204)

            query = f"UPDATE sm_users SET {', '.join(fields)} WHERE id = %s"
            values.append(user_id)  # Add user_id for WHERE clause

            cursor.execute(query, tuple(values))
            self.conn.commit()
            rowcount = cursor.rowcount
            cursor.close()

            if rowcount > 0:
                return make_response({"message": "Updated successfully."}, 201)
            else:
                return make_response({"message": "No rows updated."}, 204)

        except Exception as e:
            return {"error": str(e)}
        

    # delete profile method
    def user_deleteprofile_model(self, id):
        try:
            cursor = self.conn.cursor()
            query = " DELETE FROM sm_users WHERE ID = %s "

            values = (id,)
            cursor.execute(query, values)
            affected_rows = cursor.rowcount
            cursor.close()
            if affected_rows > 0:
                return make_response({"message": "User Deleted successfully"}, 200)
            else:
                return make_response(
                    {"message": "Nothing to delete or user not found"}, 202
                )

        except Exception as e:
            return {"error": str(e)}
        
# user login model
    def user_login_model(self, data):
        try:
            cursor = self.conn.cursor(dictionary=True)

            query = "SELECT id, role_id, email, name, phone FROM sm_users WHERE email=%s AND password=%s"
            cursor.execute(query, (data['email'], data['password']))
            result = cursor.fetchall()
            cursor.close()
            if len(result) == 1:
                userdata = result[0]
                exptime = datetime.now() + timedelta(minutes=15)
                exp_epoc_time = exptime.timestamp()
                payload = {
                    "payload":userdata,
                    "exp":int(exp_epoc_time)
                }
                jwt_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

                return make_response({"token":jwt_token}, 200)
            else:
                return make_response({"message": "NO SUCH USER"}, 204)
        except Exception as e:
            return make_response({"error": str(e)}, 500)

