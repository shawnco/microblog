from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import LoginForm, NewpostForm, RegistrationForm, EditpostForm
from app.models import Post, User
import sys
import json
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In to the Flask', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    content = ''
    form = NewpostForm()
    if form.validate_on_submit():
        content = 'Post added'
        new_post = Post(title = request.form.get('title'), body = request.form.get('text'))
        db.session.add(new_post)
        db.session.commit()
    return render_template('newpost.html', content = content, form = form)

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def editpost(id):
    if request.method == 'POST':
        form = EditpostForm()
        if form.validate_on_submit():
            edit_post = Post.query.get(id)
            edit_post.title = request.form.get('title')
            edit_post.body = request.form.get('text')
            db.session.commit()
            return redirect('/posts')
    else:
        src = Post.query.get(id)
        src.text = src.body
        form = EditpostForm(obj=src)
        return render_template('edit.html', form=form)



@app.route('/delete/<id>')
@login_required
def delete(id):
    delete_post = Post.query.get(id)
    db.session.delete(delete_post)
    db.session.commit()
    return render_template('delete.html')

@app.route('/posts')
def posts():
    content = Post.query.all()
    return render_template('posts.html', content = content)

@app.route('/post/<id>')
def post(id):
    content = Post.query.get(id)
    return render_template('post.html', content = content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)