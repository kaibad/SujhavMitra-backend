from app import app
from model.book_recommend_model import BookRecommendModel


@app.route("/recommend/book")
def book_recommend_controller():
    recommender = BookRecommendModel()
    return recommender.book_recommend_model()
