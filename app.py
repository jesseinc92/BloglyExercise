"""Blogly application."""

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'blahblah62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect_db(app)
# db.create_all()


@app.route('/')
def user_home():
    '''Displays a list of saved users.'''

    users = [User(first_name='Steve', last_name='Knocks'),
            User(first_name='Ronny', last_name='Woodburn'),
            User(first_name='Jesse', last_name='Hill'),
            User(first_name='Howdy', last_name='Doody')]

    return render_template('users.html', users=users)

