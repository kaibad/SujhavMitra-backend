from app import app
from flask import request, jsonify
from model.movie_recommend_model import MovieRecommendModel

recommender = MovieRecommendModel()

@app.route("/recommend/movie", methods=["GET"])
def movie_recommend_controller():
    raw_title = request.args.get("title")
    
    if not raw_title:
        all_movies = recommender.get_popular_movies()
        return all_movies
    
    title = raw_title.strip().strip('"').strip("'")
    result = recommender.movie_recommend_model(title)

    return result