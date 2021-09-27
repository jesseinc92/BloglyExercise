"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime


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


@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    '''Displays new post form for a specific user.'''
    
    if request.method == 'GET':
    
        user = User.query.get(user_id)
    
        return render_template('new-post.html', user=user)
    
    if request.method == 'POST':
        
        # create a class instance using the form data
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now()
        
        new_post = Post(title=title, content=content, created_at=created_at, owning_user=user_id)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f'/users/{user_id}')
    
    
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Displays an individual post's details.'''
    
    post = Post.query.get(post_id)
    
    return render_template('post-details.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    '''Shows a form to edit a post.'''
    
    if request.method == 'GET':
        
        post = Post.query.get(post_id)
        
        return render_template('edit-post.html', post=post)
    
    if request.method == 'POST':
        
        title = request.form['title']
        content = request.form['content']
        
        updated_post = Post.query.get(post_id)
        updated_post.title = title
        updated_post.content = content
        
        db.session.commit()
        
        return redirect(f'/posts/{post_id}')
    
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Deletes a post and redirects back to a user screen.'''
    
    post = Post.query.filter_by(id=post_id)
    post.delete()
    
    db.session.commit()
    
    return redirect(f'/users')