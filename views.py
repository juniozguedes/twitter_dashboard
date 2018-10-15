from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, request, redirect, url_for, render_template, session
from models import Tweets, User
from urlparse import urlparse, urljoin
from datetime import datetime
import itertools
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

@app.route('/')
def root():
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    tweets =  Tweets.query.all()
    for a in tweets:
        return (a.content)

@app.route('/home')
@login_required
def home():
	u = current_user
    	return (u.password)

@app.route('/afbase/login')
def login():
    #session['next'] = request.args.get('next')
    return render_template('login.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and \
        ref_url.netloc == test_url.netloc

@app.route('/logmein', methods=['POST'])
def logmein():
    password = request.form['password']

    user = User.query.filter_by(password=password).first()

    if not user:
        return '<h1>User not found </h1>'

    login_user(user, remember=True)

    if 'next' in session:
        next = session['next']

        if is_safe_url(next):
            return redirect(next)

@app.route('/afbase/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('afbase'))