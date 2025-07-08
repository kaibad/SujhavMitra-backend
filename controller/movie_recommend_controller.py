from app import app
from model.movie_recommend_model import MovieRecommendModel


@app.route("/recommend/movie")
def movie_recommend_controller():
    recommender = MovieRecommendModel()
    return recommender.movie_recommend_model()
