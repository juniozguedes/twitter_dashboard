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

followers = db.Table('followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
  )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    nickname = db.Column(db.String(30))
    password = db.Column(db.String(100))
    tweets = db.relationship('Tweets', backref='user', lazy=True)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    followed = db.relationship(
      'User', secondary=followers,
      primaryjoin = (followers.c.follower_id == id),
      secondaryjoin = (followers.c.followed_id == id),
      backref = db.backref('followers', lazy = 'dynamic'), lazy='dynamic')

    def follow(self, user):
      if not self.is_following(user): #Mover para o controller
        self.followed.append(user)

    def unfollow(self, user):
      if self.is_following(user):
        self.followed.remove(user)

    def is_following(self, user):
      return self.followed.filter(followers.c.followed_id == user.id).count()> 0

    def followed_posts(self):
      followed = Tweets.query.join(
        followers, (followers.c.followed_id == Tweets.tweet_owner)).filter(
          followers.c.follower_id == self.id)
      own = Tweets.query.filter_by(tweet_owner = self.id)
      return followed.union(own).order_by(Tweets.id.desc())

    def count_followers(self):
      u1 = User.query.filter_by(id=self.id).first()
      followers = u1.followers.count()
      return followers

    def count_followed(self):
      u1 = User.query.filter_by(id=self.id).first()
      followed = u1.followed.count()
      return followed

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

  if user_id is None:
    folllowers = query.all()
    return followers

  return User.query.get(int(user_id))