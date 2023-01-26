from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",
                           book_name=list(popular_df["Book-Title"].values),
                           author=list(popular_df["Book-Author"].values),
                           rating=list(popular_df["avg-ratings"].values),
                           votes=list(popular_df["num-ratings"].values),
                           image=list(popular_df["Image-URL-L"].values)
    )
                           


@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html", book_name=list(popular_df["Book-Title"].values))


@app.route("/recommend_books", methods=["post"])
def recommend():
    y = request.form.get("user_input")
    x = y if y in list(
        popular_df["Book-Title"].values) else "The Da Vinci Code"
    user_input = x if x != "" else "The Da Vinci Code"
    index = np.where(pt.index == user_input)[0][0]
    distances = similarity_score[index]
    similar_items = sorted(list(enumerate(distances)),
                           key=lambda x: x[1], reverse=True)[1:9]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Image-URL-M"].values))
        data.append(item)
    return render_template("recommend.html", data=data, user_input=user_input, book_name=list(popular_df["Book-Title"].values))


@app.route("/recommend_books1", methods=["post"])
def recommend1():
    book_name = list(popular_df["Book-Title"].values)
    for key in request.form:
        id = key
    user_input = book_name[int(id)]
    index = np.where(pt.index == user_input)[0][0]
    distances = similarity_score[index]
    similar_items = sorted(list(enumerate(distances)),
                           key=lambda x: x[1], reverse=True)[1:9]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates(
            "Book-Title")["Image-URL-M"].values))
        data.append(item)
    return render_template("recommend.html", data=data, user_input=user_input, book_name=list(popular_df["Book-Title"].values))


@app.route("/about")
def contact_ui():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
