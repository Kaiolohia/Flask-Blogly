"""Blogly application."""

import re
from flask import Flask, render_template, redirect, request, flash
from sqlalchemy.orm import session
from models import db, connect_db, User

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

@app.route('/', methods = ["POST"])
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
    return render_template('user.html', user = cur_user)

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
    User.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/')