from app import app
from flask import request, jsonify
from model.book_recommend_model import BookRecommendModel

recommender = BookRecommendModel()

@app.route("/recommend/book", methods=["GET"])
def book_recommend_controller():
    raw_title = request.args.get("title")
    if not raw_title:
        Popular_books = recommender.get_popular_book_title()
        return  Popular_books
    
    # Normalize title input
    title = raw_title.strip().strip('"').strip("'").lower()
    result=recommender.book_recommend_model(title)

    return result

@app.route("/book/<isbn>", methods=["GET"])
def get_book_by_isbn_controller(isbn):
    return recommender.get_book_by_isbn(isbn)
