import flask
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
EMPTY_POSTER = os.getenv("EMPTY_POSTER")
WIKISEARCH_BASE = os.getenv("WIKISEARCH_BASE")
GENREMAP_URL = os.getenv("GENREMAP_URL") + api_key


@app.route("/")
def index():
    selection = [
        "Monsters Inc",
        "Shang Chi",
        "teen titans",
        "jumanji",
        "Avatar",
        "Mortal Kombat",
        "The Incredibles",
        "Spiderman No Way Home",
    ]
