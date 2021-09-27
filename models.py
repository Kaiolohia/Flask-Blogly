"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import backref

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, )

    first_name = db.Column(db.Text, nullable = False, unique = True)

    last_name = db.Column(db.Text, nullable = False, unique = True)

    image_url = db.Column(db.Text)

class Post(db.Model):
    """Posts model"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    
    title = db.Column(db.Text, nullable = False, unique = True)

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(db.DateTime, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref="posts")
