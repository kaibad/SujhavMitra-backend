from app import app
from flask import request, jsonify
from model.book_recommend_model import BookRecommendModel


@app.route("/recommend/book", methods=["GET"])
def book_recommend_controller():
    raw_title = request.args.get("title")
    recommender = BookRecommendModel()
    if not raw_title:
        Popular_books = recommender.get_popular_book_title()
        return jsonify({"popular_books": Popular_books})
    
    # Normalize title input
    title = raw_title.strip().strip('"').strip("'").lower()
    result=recommender.book_recommend_model(title)

    return jsonify(result)
