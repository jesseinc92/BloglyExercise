"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    '''Conntect to database.'''

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User model that includes key components of a User object.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default='/assets/blank_photo.jpg')
    
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    

class Post(db.Model):
    '''Post model to describe post details.'''
    
    __tablename__ = 'posts'
    
    def __repr__(self):
        return f'<Post title={self.title} content={self.content} user={self.owning_user}>'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    owning_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')
    
    
class Tag(db.Model):
    '''Model to build tags.'''
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    posts = db.relationship('Post', secondary='post_tag', backref='tags')
    
    
class PostTag(db.Model):
    '''Table that references both tags and posts.'''
    
    __tablename__ = 'post_tag'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)