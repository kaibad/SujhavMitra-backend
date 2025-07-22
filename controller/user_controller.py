from app import app
from model.user_model import user_model

obj = user_model()

@app.route("/user/all", methods=["GET"])
def all_users():
    return obj.all_user_model()