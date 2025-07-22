from app import app
from flask import request
from model.user_model import user_model

obj = user_model()

@app.route("/user/all", methods=["GET"])
def all_users():
    return obj.all_user_model()

@app.route("/user/signup", methods=["POST"])
def user_signup_controller():
    return obj.signup_user_model(request.form)