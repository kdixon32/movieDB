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
    sender = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return "<Movie %r" % self.rate
