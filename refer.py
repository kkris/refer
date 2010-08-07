#!/usr/bin/env python

from flask import Flask, render_template, url_for, session, request, flash, \
                    redirect, abort
from forms import LoginForm, PostForm, CommentForm

import database


SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'secret'
DEBUG = True

refer = Flask(__name__)
refer.config.from_object(__name__)

db = database.Database()


@refer.route('/')
def index():
    posts = db.get_posts()
    return render_template('show_posts.html', posts=posts)


@refer.route('/posts/<url>')
def show_post(url, form=None):
    if form is None:
        form = CommentForm()
    post = db.get_post(url)
    return render_template('show_post.html', post=post, form=form)


@refer.route('/add-comment/<url>', methods=['POST'])
def add_comment(url):
    form = CommentForm()
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        comment = form.comment.data
        db.add_comment(url, author, email, comment)
        return redirect(url_for('show_post', url=url))
    return show_post(url=url, form=form)


@refer.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data.replace('\r\n', '<br>')
        tags = form.tags.data.split()
        db.add_post(title, post, tags)
        return redirect(url_for('index'))

    return render_template('add_post.html', form=form)


@refer.route('/search/<tag>', methods=['GET'])
def search_for_tag(tag):
    posts = db.search_for_tag(tag)
    return render_template('show_posts.html', posts=posts)


@refer.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != refer.config['USERNAME']:
            flash('Invalid login data')
        elif form.password.data != refer.config['PASSWORD']:
            flash('Invalid login data')
        else:
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@refer.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index')) 


if __name__ == '__main__':
    refer.run()

