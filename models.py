from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #if unauthorized, redirects to login
login_manager.login_message = 'You need to login!'

migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    nickname = db.Column(db.String(30))
    password = db.Column(db.String(100))
    tweets = db.relationship('Tweets', backref='user', lazy=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    followers = db.Column(ARRAY(db.Text))
    following = db.Column(ARRAY(db.Text))

class Tweets(db.Model):

    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_nickname = db.Column(db.String(30))
    owner_username = db.Column(db.String(30))
    content = db.Column(db.Text)
    entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    uniquekey = db.Column(db.Text, unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))