from flask import Flask, render_template, request
import os
import random
import requests
from dotenv import find_dotenv, load_dotenv

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


@app.route("/")
def index():
    selection = [
        "Monsters Inc",
        "Shang Chi",
        "Teen titans",
        "Jumanji",
        "Interstellar",
        "Mortal Kombat",
        "The Incredibles",
        "Spiderman No Way Home",
    ]
    search = random.choice(selection)
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
    genremap = requests.get(GENREMAP_URL)
    genremap_json = genremap.json()

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
    return render_template(
        "index.html",
        len=len(items),
        items=items,
        image=image,
        genre=genre,
        tagline=tagline,
        wikipage=wikipage,
    )


@app.route("/movie_page")
def movie():
    search = search


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
