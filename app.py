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
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("postgresurl")
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


@app.route("/index", methods=["POST", "GET"])
def index():
    selection = [  # this list holds possible queries when refreshing the index page
        "Monsters Inc",
        "Shang Chi",
        "Teen titans GO",
        "Interstellar",
        "Captain America Civil War",
        "The Incredibles 2",
        "Spiderman 2",
    ]
    search = random.choice(selection)
    if request.method == "POST":
        search = request.form["searchbox"]
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


@login_required
@app.route("/moviepage", methods=["POST", "GET"])
def moviepage():  # This function controls the individual movie pages containing the comments and ratings
    item = request.args.get("item")
    image = request.args.get("image")
    genre = request.args.get("genre")
    tagline = request.args.get("tagline")
    wikipage = request.args.get("wikipage")
    choice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    if request.method == "POST":  # This is where new comments are added to the database
        entry = request.form.get("comment-box")
        entry2 = request.form.get("rate")
        entry3 = request.form.get("item")
        item = request.form.get("item")
        image = request.form.get("image")
        genre = request.form.get("genre")
        tagline = request.form.get("tagline")
        wikipage = request.form.get("wikipage")
        newcomment = Rating(
            comment=entry, rate=entry2, title=entry3, sender=current_user.username
        )
        db.session.add(newcomment)
        db.session.commit()  # a new comment contained the users name, their thoughts, and a rating is created

    thismovie = Rating.query.filter_by(title=item)
    commentlist = []
    ratinglist = []
    userlist = []
    for i in thismovie:
        commentlist.append(i.comment)
        ratinglist.append(i.rate)
        userlist.append(i.sender)
    return render_template(
        "movie.html",
        item=item,
        image=image,
        genre=genre,
        tagline=tagline,
        wikipage=wikipage,
        choice=choice,
        commentlist=commentlist,
        ratinglist=ratinglist,
        userlist=userlist,
        len=len(commentlist),
    )


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        entry = request.form.get("username")
        try:  # this try/except keeps users on the login page until they have successfully logged in
            verifyuser = User.query.filter_by(username=entry).first()
            login_user(verifyuser)
        except:
            flask.flash("Incorrect Username Entered")
            return render_template("login.html")
        return flask.redirect(flask.url_for("index"))
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if (
            db.session.query(User.id)
            .filter_by(username=request.form.get("username"))
            .scalar()
            is None
        ):
            entry = request.form.get("username")
            newuser = User(username=entry)
            db.session.add(newuser)
            db.session.commit()  # a new user's username is saved to the database
            return flask.redirect(flask.url_for("login"))
        return flask.redirect(flask.url_for("login"))
    return render_template("signup.html")


def moviesearch(search):
    search = str(
        search
    )  # These lists are needed to produce the list of movies on the main page
    items = []
    image = []
    genre = []
    tagline = []
    wikipage = []
    forbidden_chars = "'[]"

    query_url = (
        SEARCH_URL + search
    )  # this project originally had a search bar. It may be making a return later.
    response = requests.get(query_url)
    response_json = response.json()
    movies = response_json
    total = len(movies["results"])
    for movie in range(
        total
    ):  # This for loop populates the lists with movie information
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
