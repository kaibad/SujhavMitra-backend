# auth_model.py
from datetime import datetime, timedelta
import mysql.connector
import jwt
from flask import make_response, request, json
import re
from configs.config import dbconfig, JWT_SECRET
from functools import wraps

class auth_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=dbconfig["host"],
                port=dbconfig["port"],
                user=dbconfig["username"],
                password=dbconfig["password"],
                database=dbconfig["database"],
                autocommit=True
            )
            print("Auth DB Connection established")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args, **kwargs):
                if not self.conn:
                    return make_response({"ERROR": "DATABASE_CONNECTION_ERROR"}, 500)
                
                endpoint = request.url_rule.rule
                print(f"Checking auth for endpoint: {endpoint}")
                
                # Get Authorization header
                authorization = request.headers.get("authorization")
                
                # Validate Bearer token format
                if not authorization or not re.match(r"^Bearer\s+[^ ]+$", authorization):
                    return make_response({"ERROR": "INVALID_TOKEN"}, 401)
                
                # Extract token from header
                token = authorization.split(" ")[1]
                
                try:
                    # Decode JWT token
                    tokendata = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                    current_role = tokendata['payload']['role_id']
                    
                    # Create cursor for this operation
                    cursor = self.conn.cursor(dictionary=True)
                    
                    # Fetch allowed roles for the given endpoint
                    cursor.execute(
                        "SELECT role_id FROM accessibility_view WHERE endpoint = %s",
                        (endpoint,),
                    )
                    rows = cursor.fetchall()
                    cursor.close()
                    
                    if not rows:
                        return make_response({"ERROR": "UNKNOWN_ENDPOINT"}, 404)
                    
                    # Extract allowed role IDs
                    allowed_roles = [row["role_id"] for row in rows]
                    
                    # Check if user role is allowed
                    if current_role in allowed_roles:
                        return func(*args, **kwargs)
                    else:
                        return make_response({"ERROR": "ACCESS_DENIED"}, 403)
                    
                except jwt.ExpiredSignatureError:
                    return make_response({"ERROR": "TOKEN_EXPIRED"}, 401)
                except jwt.InvalidTokenError:
                    return make_response({"ERROR": "INVALID_TOKEN"}, 401)
                except Exception as e:
                    print(f"Token auth error: {e}")
                    return make_response({"ERROR": "AUTHENTICATION_ERROR"}, 500)
            return inner2
        return inner1
