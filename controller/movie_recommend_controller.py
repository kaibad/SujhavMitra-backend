from app import app
from flask import request, jsonify
from model.movie_recommend_model import MovieRecommendModel


@app.route("/recommend/movie", methods=["GET"])
def movie_recommend_controller():
    raw_title = request.args.get("title")
    recommender = MovieRecommendModel()
    if not raw_title:
        all_movies = recommender.get_all_movie_titles()
        return jsonify({"all_movies": all_movies})
    
    title = raw_title.strip().strip('"').strip("'")
    result = recommender.movie_recommend_model(title)

    return jsonify(result)