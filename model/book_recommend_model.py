import pickle
from flask import make_response

class BookRecommendModel:
    def __init__(self):
        import pickle
        with open("models/books.pkl", "rb") as f:
            self.books = pickle.load(f)
        with open("models/popular_books_df.pkl", "rb") as f:
            self.popbooks = pickle.load(f)
        with open("models/similarity_scores.pkl", "rb") as f:
            self.similarity = pickle.load(f)
        with open("models/book_user_matrix.pkl", "rb") as f:
            self.book_user_matrix = pickle.load(f)

        # Normalize titles for lookup
        self.book_index_titles = list(self.book_user_matrix.index.str.lower().str.strip())

    def get_popular_book_title(self):
        popular_titles = self.popbooks["Book-Title"].unique()[:15]
        popular_books_info = []
        for title in popular_titles:
            book_info = self.books[self.books["Book-Title"] == title].drop_duplicates("Book-Title")

             # If book info exists, add its details to the list
            if not book_info.empty:
                popular_books_info.append({
                    "title": book_info["Book-Title"].values[0],
                    "author": book_info["Book-Author"].values[0],
                    "isbn": book_info["ISBN"].values[0],
                    "publishdate": book_info["Year-Of-Publication"].values[0],
                    "publisher": book_info["Publisher"].values[0],
                    "imageurl": book_info["Image-URL-L"].values[0]
                })

        return make_response({"popular_books": popular_books_info},200)


    def book_recommend_model(self, title):
        norm_title = title.strip().lower()

        if norm_title not in self.book_index_titles:
            return {"error": f"Book titled '{title}' not found"}

        book_index = self.book_index_titles.index(norm_title)
        distances = self.similarity[book_index]
        book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = []
        for i in book_list:
            similar_title = self.book_user_matrix.index[i[0]]

            # Find full book info (title, author, ISBN) — drop duplicates to avoid multiple editions
            book_info = self.books[self.books["Book-Title"] == similar_title].drop_duplicates("Book-Title")

            if not book_info.empty:
                recommendations.append({
                    "title": book_info["Book-Title"].values[0],
                    "author": book_info["Book-Author"].values[0],
                    "isbn": book_info["ISBN"].values[0],
                    "publishdate":book_info["Year-Of-Publication"].values[0],
                    "publisher":book_info["Publisher"].values[0],
                    "imageurl":book_info["Image-URL-L"].values[0]
                })

        return make_response({"recommendations": recommendations},200)
