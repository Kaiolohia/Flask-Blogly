"""
TODO:
    Get tag "buttons" to be better styled
"""

"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = 'nimdA'


connect_db(app)
db.create_all()

@app.route('/')
def show_home_page():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/users/new')
def show_new_user_page():
    return render_template('create_user.html')

@app.route('/users/new', methods = ["POST"])
def add_new_user():
    name_f = request.form['name_f']
    name_l = request.form['name_l']
    pfplink = request.form['pfp']
    newUser = User(first_name = name_f, last_name = name_l, image_url = pfplink)
    db.session.add(newUser)
    db.session.commit()
    return redirect('/')

@app.route('/users/<id>')
def show_user(id):
    cur_user = User.query.filter_by(id = id).first_or_404()
    users_posts = Post.query.filter_by(user_id = id).all()
    return render_template('user.html', user = cur_user, users_posts = users_posts)

@app.route('/users/<id>/edit')
def edit_user(id):
    cur_user = User.query.filter_by(id = id).first_or_404()
    return render_template('edit_user.html', user = cur_user)

@app.route('/users/<id>/edit', methods = ["POST"])
def update_user(id):
    cur_user = User.query.filter_by(id = id).first_or_404()
    if request.form['name_f']:
        cur_user.first_name = request.form['name_f']
    if request.form['name_l']: 
        cur_user.last_name = request.form['name_l']
    if request.form['pfp']: 
        cur_user.image_url = request.form['pfp']
    db.session.commit()
    flash(f"Updated user {cur_user.first_name} {cur_user.last_name}")
    return redirect('/')

@app.route('/users/<id>/delete')
def delete_user(id):
    cur_user = User.query.filter_by(id = id).first_or_404()
    flash(f"Delted user {cur_user.first_name} {cur_user.last_name}")
    db.session.delete(cur_user)
    db.session.commit()
    return redirect('/')

"""
vvvv PART 2 ROUTES vvvv
"""

@app.route('/users/<id>/posts/new')
def show_new_post_page(id):
    #display new post form
    return render_template('new_post.html', id = id, tags = Tag.query.all())

@app.route('/users/<id>/posts/new', methods = ["POST"])
def handle_new_post(id):
    #handle new post request
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title = title, content = content, user_id = id, created_at = datetime.now(), tags = tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route('/posts/<id>')
def show_post(id):
    #show post content
    post = Post.query.filter_by(id = id).first_or_404()
    print(PostTag.query.filter_by(post_id = id).all())
    return render_template('post.html', post = post)

@app.route('/posts/<id>/edit')
def edit_post(id):
    #show edit post page
    cur_post = Post.query.filter_by(id = id).first_or_404()
    return render_template('edit_post.html',
    post = cur_post, 
    tags = Tag.query.all(),
    )

@app.route('/posts/<id>/edit', methods = ["post"])
def handle_edit_post(id):
    #handle edited post
    cur_post = Post.query.filter_by(id = id).first_or_404()
    cur_post.title = request.form['title']
    cur_post.content = request.form['content']
    tags = request.form.getlist('tags')
    PostTag.query.filter_by(post_id = id).delete()
    for tag in tags:
        new_tag = PostTag(post_id = id, tag_id = tag)
        db.session.add(new_tag)
    db.session.commit()
    flash("Updated post")
    return redirect(f'/posts/{id}')

@app.route('/posts/<id>/delete')
def delete_post(id):
    #delete posts
    post = Post.query.filter_by(id=id).first_or_404()
    flash(f"Deleted post {post.title}")
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

"""
vvvv Part 3 routes vvvv
"""

@app.route('/tags')
def show_all_tags():
    #show all tags
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<id>')
def show_tag_details(id):
    #send tag data
    return render_template('tag.html', tag = Tag.query.filter_by(id = id).first_or_404())

@app.route('/tags/new')
def show_new_tag_page():
    #show new tag form
    return render_template('new_tag.html')

@app.route('/tags/new', methods=["POST"])
def handle_new_tag():
    #handle new tag
    new_tag = Tag(name = request.form["name"])
    db.session.add(new_tag)
    db.session.commit()
    flash(f"Added tag {new_tag.name}")
    return redirect('/tags')

@app.route('/tags/<id>/edit')
def show_edit_tag_page(id):
    #show edit tag form
    return render_template('edit_tag', tag = Tag.query.filter_by(id = id).first_or_404())

@app.route('/tags/<id>/edit', methods=["POST"])
def handle_edit_tag(id):
    #handle edited tag
    cur_tag = Tag.query.filter_by(id = id).first_or_404()
    cur_tag.name = request.form["name"]
    flash('Edited tag')
    return redirect('/tags')

@app.route('/tags/<id>/delete')
def delete_tag(id):
    #handle deleting tag
    tag = Tag.query.filter_by(id = id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash(f'Deleted tag {tag.name}')
    return redirect('/tags')