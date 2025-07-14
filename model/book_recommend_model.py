class BookRecommendModel:
    def __init__(self):
        with open("models/books.pkl", "rb") as f:
            self.books = pickle.load(f)
        with open("models/similarity_scores.pkl", "rb") as f:
            self.similarity = pickle.load(f)

    def book_recommend_model(self, title):
        if title not in self.books["title"].values:
            return {"error": "Book not found"}

        index = self.books[self.books["title"] == title].index[0]
        distances = self.similarity[index]
        book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = [self.books.iloc[i[0]].title for i in book_list]
        return {"recommendations": recommendations}
