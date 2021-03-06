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
    return redirect(url_for('timeline'))

@app.route('/twitter', methods=['POST', 'GET'])
@login_required
def timeline():
    if request.method == 'POST':
        tweet = Tweets(content=request.form['tweet'], tweet_owner=current_user.id)
        owner_id = tweet.tweet_owner
        owner = User.query.filter_by(id=owner_id).first()
        tweet.owner_nickname = owner.nickname
        tweet.owner_username = owner.username
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('timeline'))    
    elif request.method == 'GET':
        uid = current_user.id
        user = User.query.filter_by(id=uid).first()
        tweets = user.followed_posts()
        followers = user.count_followers()
        followed = user.count_followed()
        #all_tweets = Tweets.query.filter().order_by(Tweets.id.desc()).all()        
        return render_template('timeline.html', tweets = tweets, user = user, followers=followers, followed=followed)

@app.route('/twitter/profile/tl/<int:id>', methods=['GET', 'POST', 'DELETE'])
def profile_timeline(id):
    if request.method == 'POST':
        tweet = Tweets(content=request.form['tweet'], tweet_owner=current_user.id)
        owner_id = tweet.tweet_owner
        owner = User.query.filter_by(id=owner_id).first()
        tweet.owner_nickname = owner.nickname
        tweet.owner_username = owner.username
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('profile', id = current_user.id))  

    elif request.method == 'DELETE':
        tweet = Tweets.query.filter_by(id=id).first() #Mandar para o controller
        db.session.delete(tweet) #Mandar para o controller
        db.session.commit() #Mandar para o controller
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        i = User.query.filter_by(id=current_user.id).first()
        user = User.query.filter_by(id=id).first()
        user_tweets = Tweets.query.filter_by(tweet_owner=id).order_by(Tweets.id.desc()).all()
        followers = user.count_followers()
        followed = user.count_followed()
        return render_template('profile.html', user = user, user_tweets = user_tweets, i=i)

@app.route('/twitter/<int:id>', methods=['GET', 'DELETE'])
def show(id):
    tweet = Tweets.query.filter_by(id=id).first()

    if request.method == 'DELETE':
        db.session.delete(tweet)
        db.session.commit()
        return redirect(url_for('timeline'))

@app.route('/twitter/follow/<int:id>', methods=['POST'])
def follow(id):
    if request.method == 'POST':
        i = User.query.filter_by(id=current_user.id).first()
        user = User.query.filter_by(id=id).first()

        i.follow(user)
        db.session.commit()
        return redirect(url_for('profile_timeline', id=id))

@app.route('/twitter/unfollow/<int:id>', methods=['POST'])
def unfollow(id):
    if request.method == 'POST':
        i = User.query.filter_by(id=current_user.id).first()
        user = User.query.filter_by(id=id).first()

        i.unfollow(user)
        db.session.commit()
        return redirect(url_for('profile_timeline', id=id))

@app.route('/twitter/u/following')
def following():
        i = User.query.filter_by(id=current_user.id).first()
        following = i.followed.all()
        return render_template('following.html', user = i, following = following)

@app.route('/twitter/u/followers')
def followers():
        i = User.query.filter_by(id=current_user.id).first()
        followers = i.followers.all()
        return render_template('followers.html', user = i, followers = followers)

@app.route('/twitter/<int:id>/following')
def following_profile():
        u = User.query.filter_by(id=id).first()
        following = u.followed.all()
        return render_template('following.html', user = u, following = following)

@app.route('/twitter/<int:id>/followers')
def followers_profile():
        u = User.query.filter_by(id=id).first()
        followers = u.followers.all()
        return render_template('followers.html', user = u, followers = followers)

@app.route('/home')
@login_required
def home():
	return str((current_user.id))

@app.route('/twitter/login')
def login():
    #session['next'] = request.args.get('next')
    return render_template('login.html')

@app.route('/logmein', methods=['POST'])
def logmein():
    login = request.form['login']
    u = User.query.filter_by(username=login).first()
    check = check_password_hash(u.password, request.form['password']) 
    if not u:
        return '<h1>User not found </h1>'
    elif not check: 
        return '<h1>Wrong password </h1>'

    login_user(u, remember=True)
    #if 'next' in session:
    #    next = session['next']
    #    if is_safe_url(next):
    return redirect(url_for('timeline'))

@app.route('/twitter/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('root'))

@app.route('/twitter/register')
def registration():
    return render_template('register.html')

@app.route('/twitter/register', methods=['POST'])
def register():
    login = request.form['login']
    password = generate_password_hash(request.form['password'])
    nickname = request.form['nickname']
    u = User(username=login,password=password, nickname=nickname)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('login'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and \
        ref_url.netloc == test_url.netloc