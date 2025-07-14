import pickle

class MovieRecommendModel:
    def __init__(self):
        with open("models/movie_list.pkl", "rb") as f:
            self.movies = pickle.load(f)
        with open("models/similarity_books.pkl", "rb") as f:
            self.similarity = pickle.load(f)
    
    def get_all_movie_titles(self):
        return self.movies["title"].tolist()

    def movie_recommend_model(self, title):
        if title not in self.movies["title"].values:
            return {"error": "Movie not found"}

        index = self.movies[self.movies["title"] == title].index[0]
        distances = self.similarity[index]

        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        recommendations = [self.movies.iloc[i[0]].title for i in movie_list]
        return {"recommendations": recommendations}
