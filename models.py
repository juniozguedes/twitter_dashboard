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
    password = db.Column(db.String(20))
    tweets = db.relationship('Tweets', backref='user')
    name = db.Column(db.String(30))

class Tweets(db.Model):

    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    uniquekey = db.Column(db.Text, unique=True)
    
#    def __init__(self, pid, partner, description, role, multitarifa, extra, ficha):
#        self.pid = pid
 #       self.partner = partner
  #      self.description = description
   #     self.role = role
    #    self.multitarifa = multitarifa
     #   self.extra = extra
      #  self.ficha = ficha
       # self.tags = ['t_0','t_1']
        #self.remid = ['t_0','t_1']
        #self.uniquekey = generate_password_hash(str(random.randrange(1000)))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))