from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import Blogpost
import sqlite3
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@main.route('/profile', methods=['POST'])
@login_required
def usun_post():
    ident = request.form.get('id')
    if post.author != current_user:
        abort(403)
    post = Blogpost.query.filter_by(id=ident).delete()
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    content = request.form.get('content')
    editedpost = Blogpost(title=title, subtitle=subtitle, author=current_user.name, content=content, date_posted=datetime.now())

    db.session.add(editedpost)
   # db.session.delete(post)
   # db.session.commit()

    
    return render_template('edit.html', post=post, editedpost=editedpost)

@main.route('/add')
@login_required
def add():
    return render_template('add.html')

@main.route('/addpost', methods=['POST'])
def addpost():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    #author = request.form.get('author')
    content = request.form.get('content')

    post = Blogpost(title=title, subtitle=subtitle, author=current_user.name, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    posts = Blogpost.query.filter_by(author=current_user.name).all()
    return render_template('profile.html', name=current_user.name, posts=posts)