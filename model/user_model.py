import mysql.connector
from flask import make_response
from configs.config import dbconfig, JWT_SECRET
from datetime import datetime, timedelta
import jwt
import bcrypt
import re

class user_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=dbconfig["host"],
                port=dbconfig["port"],
                user=dbconfig["user"],
                password=dbconfig["password"],
                database=dbconfig["database"],
                autocommit=True
            )
            print("User DB Connection established")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        # Basic phone validation - adjust as needed
        pattern = r'^\+?[\d\s\-\(\)]{10,}$'
        return re.match(pattern, phone) is not None

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    # Get all users - for admin
    def all_user_model(self):
        if not self.conn:
            return make_response({"error": "Database connection not established"}, 500)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            # Don't return passwords
            cursor.execute("SELECT id, name, phone, email, role_id FROM sm_users")
            result = cursor.fetchall()
            cursor.close()
            
            if result:
                return make_response({"users": result}, 200)
            else:
                return make_response({"message": "No users found", "users": []}, 200)
        except Exception as e:
            print(f"Error fetching users: {e}")
            return make_response({"error": "Failed to fetch users"}, 500)

    # User signup
    def signup_user_model(self, user_data):
        if not self.conn:
            return make_response({"error": "Database connection not established"}, 500)

        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'password']
        for field in required_fields:
            if field not in user_data or not user_data[field].strip():
                return make_response({"error": f"{field} is required"}, 400)

        # Validate email format
        if not self.validate_email(user_data['email']):
            return make_response({"error": "Invalid email format"}, 400)

        # Validate phone format
        if not self.validate_phone(user_data['phone']):
            return make_response({"error": "Invalid phone format"}, 400)

        # Validate password strength
        if len(user_data['password']) < 6:
            return make_response({"error": "Password must be at least 6 characters"}, 400)

        try:
            cursor = self.conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM sm_users WHERE email = %s", (user_data['email'],))
            if cursor.fetchone():
                cursor.close()
                return make_response({"error": "Email already exists"}, 400)

            # Hash password
            hashed_password = self.hash_password(user_data['password'])
            
            query = "INSERT INTO sm_users (name, phone, email, role_id, password) VALUES (%s, %s, %s, %s, %s)"
            values = (
                user_data["name"].strip(),
                user_data["phone"].strip(),
                user_data["email"].strip().lower(),
                3,  # Default user role
                hashed_password.decode('utf-8')
            )
            
            cursor.execute(query, values)
            cursor.close()
            
            return make_response({"message": "User registered successfully"}, 201)
            
        except mysql.connector.IntegrityError as e:
            print(f"Integrity error: {e}")
            return make_response({"error": "Email already exists"}, 400)
        except Exception as e:
            print(f"Signup error: {e}")
            return make_response({"error": "Registration failed"}, 500)

    # Update user
    def update_user_model(self, user_data):
        if not self.conn:
            return make_response({"error": "Database connection not established"}, 500)

        if 'id' not in user_data:
            return make_response({"error": "User ID is required"}, 400)

        try:
            cursor = self.conn.cursor()
            user_id = user_data['id']

            fields = []
            values = []

            # Handle password separately if provided
            if 'password' in user_data and user_data['password']:
                if len(user_data['password']) < 6:
                    cursor.close()
                    return make_response({"error": "Password must be at least 6 characters"}, 400)
                
                hashed_password = self.hash_password(user_data['password'])
                fields.append("password = %s")
                values.append(hashed_password.decode('utf-8'))

            # Handle other fields
            for key, value in user_data.items():
                if key not in ["id", "password"] and value:
                    if key == "email":
                        if not self.validate_email(value):
                            cursor.close()
                            return make_response({"error": "Invalid email format"}, 400)
                        value = value.strip().lower()
                    elif key == "phone":
                        if not self.validate_phone(value):
                            cursor.close()
                            return make_response({"error": "Invalid phone format"}, 400)
                        value = value.strip()
                    elif key == "name":
                        value = value.strip()
                    
                    fields.append(f"{key} = %s")
                    values.append(value)

            if not fields:
                cursor.close()
                return make_response({"message": "Nothing to update"}, 200)

            query = f"UPDATE sm_users SET {', '.join(fields)} WHERE id = %s"
            values.append(user_id)

            cursor.execute(query, tuple(values))
            rowcount = cursor.rowcount
            cursor.close()

            if rowcount > 0:
                return make_response({"message": "User updated successfully"}, 200)
            else:
                return make_response({"message": "User not found"}, 404)

        except mysql.connector.IntegrityError as e:
            print(f"Update integrity error: {e}")
            return make_response({"error": "Email already exists"}, 400)
        except Exception as e:
            print(f"Update error: {e}")
            return make_response({"error": "Update failed"}, 500)

    # Delete user
    def user_deleteprofile_model(self, user_id):
        if not self.conn:
            return make_response({"error": "Database connection not established"}, 500)

        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM sm_users WHERE id = %s"
            cursor.execute(query, (user_id,))
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                return make_response({"message": "User deleted successfully"}, 200)
            else:
                return make_response({"message": "User not found"}, 404)

        except Exception as e:
            print(f"Delete error: {e}")
            return make_response({"error": "Delete failed"}, 500)

    # User login
    def user_login_model(self, data):
        if not self.conn:
            return make_response({"error": "Database connection not established"}, 500)

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return make_response({"error": "Email and password are required"}, 400)

        try:
            cursor = self.conn.cursor(dictionary=True)

            query = "SELECT id, role_id, email, name, phone, password FROM sm_users WHERE email = %s"
            cursor.execute(query, (data['email'].strip().lower(),))
            result = cursor.fetchone()
            cursor.close()

            if result and self.verify_password(data['password'], result['password']):
                # Remove password from user data
                user_data = {
                    'id': result['id'],
                    'role_id': result['role_id'],
                    'email': result['email'],
                    'name': result['name'],
                    'phone': result['phone']
                }
                
                # Create JWT token with longer expiry
                exptime = datetime.now() + timedelta(hours=24)
                exp_epoc_time = exptime.timestamp()
                
                payload = {
                    "payload": user_data,
                    "exp": int(exp_epoc_time)
                }
                
                jwt_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
                
                return make_response({"token": jwt_token}, 200)
            else:
                return make_response({"message": "Invalid email or password"}, 401)
                
        except Exception as e:
            print(f"Login error: {e}")
            return make_response({"error": "Login failed"}, 500)

