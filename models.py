from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config["SECRET_KEY"] = 'this is my "secret" key'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
