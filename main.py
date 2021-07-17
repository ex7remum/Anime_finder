import sys

from flask import Flask, render_template, request
from clients import FindAnimeByGenres, FindAnimeByURL

app = Flask(__name__)
anime_by_url = FindAnimeByURL()
anime_by_genres = FindAnimeByGenres()


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. "
            f"Try going to '/form' to submit form"
        )
    if request.method == "POST":
        if "picture_url" in request.form:
            form_data = anime_by_url(request.form["picture_url"])
        else:
            genres = request.form["genres"].split(", ")
            for i in range(len(genres)):
                genres[i] = genres[i].lower()
            form_data = anime_by_genres(genres)
        if form_data["message"] == "ok":
            return render_template("data.html", form_data=form_data)
        else:
            return render_template("error.html", form_data=form_data)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
