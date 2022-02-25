from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Rating(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    comment = db.Column(db.String(50), unique=True, nullable=False)
    rate = db.Column(db.String(2), unique=True, nullable=False)

    def __repr__(self):
        return "<Movie %r" % self.rate
