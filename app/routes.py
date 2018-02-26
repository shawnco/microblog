from app import app, db
from flask import render_template, request
from app.forms import LoginForm, NewpostForm
from app.models import Post
import sys
import json

@app.route('/')
@app.route('/index')
def index():
    content = "'Ello guvna! Fancy some fish 'n chips with ya afternoon tea?"
    return render_template('index.html', content = content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('validate login',file=sys.stderr)
        flash('Login requested for {}, remember_me = {}').format(
            form.username.data, form.remember_me.data
        )
        return redirect('/index')
    return render_template('login.html', form=form, title='Sign In to the Madhouse')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    print('request?',request.form,file=sys.stderr)
    content = ''
    form = NewpostForm()
    if form.validate_on_submit():
        content = 'Post added'
        print('DANGIT!',request.form.get('title'),request.form.get('text'),file=sys.stderr)
        # How to add to db?
        new_post = Post(title = request.form.get('title'), body = request.form.get('text'))
        db.session.add(new_post)
        db.session.commit()
    return render_template('newpost.html', content = content, form = form)

@app.route('/modlist')
def mod_list():
    content = ['jere', 'luke', 'kinka', 'kss', 'nerdforjesus1']
    return render_template('modlist.html', content = content)

@app.route('/posts')
def posts():
    content = Post.query.all()
    return render_template('posts.html', content = content)

@app.route('/post/<id>')
def post(id):
    content = Post.query.get(id)
    return render_template('post.html', content = content)