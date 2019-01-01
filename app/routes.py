from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.urls import url_parse
from datetime import datetime

# all edits from now on are part of Fork #1. Past the original login template.

#sends a request every time a view function is executed
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    #user = {'username' : 'jc.penny7'}
    posts = [
    {'name':'Jordan','date':'1/12/2018','value':12},
    {'name':'Kayla','date':'11/13/2018','value':6},
    {'name':'Pucci','date':'4/9/2018','value':1},
    {'name':'Gucci','date':'10/28/2018','value':3},
    {'name':'Mango','date':'2/17/2018','value':9},
    {'name':'Molly','date':'6/20/2018','value':16},

    ]
    return render_template('index.html', title = 'Home', posts=posts)

@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash ('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = (url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title = "Sign In",form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, new user! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title ="Register",form=form)

@app.route('/username/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{'author':user,'body':'Test post #1'} , {'author':user,'body':'Test post #2'}]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title = 'Edit Profile',form=form)
