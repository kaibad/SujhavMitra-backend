from flask import Flask

# Flask constructor takes the name of  current module (__name__) as argument.app is a instance of the Flask app
app = Flask(__name__)

# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
@app.route("/")
# ‘/’ URL is bound with hello_world() function.
def home():
    return "Welcome to the SujhavMitra!"

from controller.book_recommend_controller import book_recommend_controller
from controller.movie_recommend_controller import movie_recommend_controller

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application on the local development server.
    app.run()