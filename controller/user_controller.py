from app import app
from flask import request
from model.user_model import user_model
from model.auth_model import auth_model

obj = user_model()
auth_obj=auth_model()

# user Get controller: this is for the admin to manage users through dashboard
@app.route("/user/all", methods=["GET"])
@auth_obj.token_auth()
def all_users():
    return obj.all_user_model()

# Signup profile controller
@app.route("/user/signup", methods=["POST"])
def user_signup_controller():
    return obj.signup_user_model(request.form)

# Update profile controller
@app.route("/user/updateProfile", methods=["PATCH"])
def patch_user():
    return obj.update_user_model(request.form)

# delete profile controller
@app.route("/user/deleteprofile/<id>", methods=["DELETE"])
def user_delete_controller(id):
    result = obj.user_deleteprofile_model(id)
    return result

@app.route("/user/login" ,  methods=["POST"])
def user_login():
    # auth_data = request.authorization

    return obj.user_login_model(request.form)

# obj.user_login_model(auth_data['username'], auth_data['password']