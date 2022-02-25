import flask
from flask import Flask, render_template, request
import os
import random
import requests
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Rating
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
api_key = os.getenv("api_key")
BASE_URL = os.getenv("BASE_URL")
SEARCH_URL = BASE_URL + api_key + "&language=en-US&query="
POSTER_URL = os.getenv("POSTER_URL")
DETAILS_URL = os.getenv("DETAILS_URL")
EMPTY_POSTER = os.getenv("EMPTY_POSTER")
WIKISEARCH_BASE = os.getenv("WIKISEARCH_BASE")
GENREMAP_URL = os.getenv("GENREMAP_URL") + api_key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/index")
def index():
    selection = [
        "Monsters Inc",
        "Shang Chi",
        "Teen titans GO",
        "Interstellar",
        "Captain America Civil War",
        "The Incredibles 2",
        "Spiderman No Way Home",
    ]
    search = random.choice(selection)

    (items, image, genre, tagline, wikipage) = moviesearch(search)
    return render_template(
        "index.html",
        len=len(items),
        items=items,
        image=image,
        genre=genre,
        tagline=tagline,
        wikipage=wikipage,
    )


@app.route("/moviepage")
def moviepage():
    item = request.args.get("item")
    image = request.args.get("image")
    genre = request.args.get("genre")
    tagline = request.args.get("tagline")
    wikipage = request.args.get("wikipage")
    choice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    comments = Rating.query.filter_by(title=item)
    ratings = Rating.query.filter_by(title=item)
    commentlist = []
    ratinglist = []

    return render_template(
        "movie.html",
        item=item,
        image=image,
        genre=genre,
        tagline=tagline,
        wikipage=wikipage,
        choice=choice,
    )


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        entry = request.form.get("username")
        verifyuser = User.query.filter_by(username=entry).first()
        login_user(verifyuser)
        return flask.redirect(flask.url_for("index"))
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        entry = request.form.get("username")
        newuser = User(username=entry)
        db.session.add(newuser)
        db.session.commit()
        return flask.redirect(flask.url_for("login"))
    return render_template("signup.html")


@app.route("/leave_rating", methods=["POST", "GET"])
def leave_rating():
    if request.method == "POST":
        entry = request.form.get("comment-box")
        entry2 = request.form.get("rate")
        entry3 = request.form.get("movietitle")
        newcomment = Rating(comment=entry, rate=entry2, title=entry3)
        db.session.add(newcomment)
        db.session.commit()
        return flask.redirect(flask.url_for("moviepage"))
    return render_template("movie.html")


def moviesearch(search):
    search = str(search)
    items = []
    image = []
    genre = []
    tagline = []
    wikipage = []
    forbidden_chars = "'[]"

    query_url = SEARCH_URL + search
    response = requests.get(query_url)
    response_json = response.json()
    movies = response_json
    total = len(movies["results"])
    for movie in range(total):
        items.append(movies["results"][movie].get("title"))
        poster_path = movies["results"][movie].get("poster_path")
        if poster_path == None:
            poster_path = EMPTY_POSTER
        else:
            poster_path = POSTER_URL + poster_path
        image.append(poster_path)
        wikisearch_url = (
            WIKISEARCH_BASE + items[movie] + "&limit=1&namespace=0&format=json"
        )
        wikiret = requests.get(wikisearch_url)
        wiki_json = wikiret.json()
        wikistr = str(wiki_json[3])
        for forbidden_char in forbidden_chars:
            wikistr = wikistr.replace(forbidden_char, "")
        wikipage.append(wikistr)
        movie_id = movies["results"][movie].get("id")
        detailsret = requests.get(DETAILS_URL + str(movie_id) + "?" + api_key)
        details_json = detailsret.json()
        tagline.append(details_json["tagline"])
        genres = ", ".join(genre["name"] for genre in details_json["genres"])
        genre.append(genres)
        return (items, image, genre, tagline, wikipage)


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
