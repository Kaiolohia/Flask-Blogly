"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

class PostTag(db.Model):
    """PostTag table"""
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)


class Tag(db.Model):
    """Tags model"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship(
        'Post',
        secondary="post_tag",
        cascade="all,delete",
        backref="tags",
    )