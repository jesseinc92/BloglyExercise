"""Blogly application."""

import re
from flask import Flask, render_template, redirect, request
from flask.wrappers import Request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'blahblah62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def user_home():
    '''Displays a list of saved users.'''

    return redirect('/users')


@app.route('/users')
def users_list():
    '''Displays a list of saved users.'''

    # query the database for all current users
    users = User.query.all()

    return render_template('users.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    '''Displays a form to create a new user.'''

    if request.method == 'GET':
        return render_template('users-form.html')
        
    if request.method == 'POST':
     
        # gather form data to commit to db
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        image_url = image_url if len(image_url) > 0 else None
        
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    '''Display individual user information.'''

    user = User.query.get(user_id)

    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    '''Display the edit form to change user data.'''

    if request.method == 'GET':
        
        # display form for user to edit details
        user = User.query.get(user_id)

        return render_template('edit.html', user=user)
    
    if request.method == 'POST':
        
        # process form inputs and update user in db
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        image_url = image_url if len(image_url) > 0 else None
        
        updated_user = User.query.get(user_id)
        updated_user.first_name = first_name
        updated_user.last_name = last_name
        updated_user.image_url = image_url
        
        db.session.commit()
        
        return redirect('/users')
    
    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Deletes a user from the database and redirects to the user list.'''
    
    
    user = User.query.filter_by(id=user_id)
    user.delete()
    
    db.session.commit()
    
    return redirect('/users')