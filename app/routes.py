from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'jc.penny7'}
    posts = [
    {'name':'Jordan','date':'1/12/2018','value':12},
    {'name':'Kayla','date':'11/13/2018','value':6},
    {'name':'Pucci','date':'4/9/2018','value':1},
    {'name':'Gucci','date':'10/28/2018','value':3},
    {'name':'Mango','date':'2/17/2018','value':9},
    {'name':'Molly','date':'6/20/2018','value':16},

    ]
    return render_template('index.html', title = 'Home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = "Sign In",form=form)
