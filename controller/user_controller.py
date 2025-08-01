from app import app
from flask import request,make_response
from model.user_model import user_model
from model.auth_model import auth_model

obj = user_model()
auth_obj=auth_model()

# Get all users - admin only
@app.route("/user/all", methods=["GET"])
@auth_obj.token_auth()
def all_users():
    return obj.all_user_model()

# User signup
@app.route("/user/signup", methods=["POST"])
def user_signup_controller():
    return obj.signup_user_model(request.form)

# Update user profile
@app.route("/user/updateProfile", methods=["PATCH"])
@auth_obj.token_auth()
def patch_user():
    return obj.update_user_model(request.form)

# Delete user profile
@app.route("/user/deleteprofile/<id>", methods=["DELETE"])
@auth_obj.token_auth()
def user_delete_controller(id):
    result = obj.user_deleteprofile_model(id)
    return result

# User login
@app.route("/user/login" ,  methods=["POST"])
def user_login():
    return obj.user_login_model(request.form)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return make_response({"error": "Endpoint not found"}, 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response({"error": "Internal server error"}, 500)
