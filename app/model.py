from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email=db.Column(db.String(255),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String())
    pass_secure=db.Column(db.String(255))
    post=db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
  

    @property
    def password(self):
        raise AttributeError ('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__= 'roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    users=db.relationship('User',backref='role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key = True)
    owner_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    title=db.Column(db.String(255), nullable=False)
    subtitle=db.Column(db.String(255),nullable=False)
    content=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(255),nullable=False)
    date=db.Column(db.DateTime)


class Comment(db.Model):

    __tablename__='comments'

    id =db.Column(db.Integer,primary_key=True)
    posts_id=db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    comment=db.Column(db.Text)
    comment_date=db.Column(db.DateTime)

    def __repr__(self):
        return f'Comment: id: {self.id} comment: {self.description}'

    @classmethod
    def get_comments(cls,user_id):
        commentsretrieved = Comment.query.filter_by(user_id=user_id).all()
        return commentsretrieved

class Quote:
    '''
    Quote class to define Quote Objects
    '''

    def __init__(self,author,quote,permalink):
        self.id =id
        self.author = author
        self.quote = quote
        self.permalink = "http://quotes.stormconsultancy.co.uk/quotes/19"

