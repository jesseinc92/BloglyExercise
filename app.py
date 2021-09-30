"""Blogly application."""

from operator import pos
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
        tags = Tag.query.all()
    
        return render_template('new-post.html', user=user, tags=tags)
    
    if request.method == 'POST':
        
        # create a class instance using the form data
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now()
        
        new_post = Post(title=title, content=content, created_at=created_at, owning_user=user_id)
        
        # commit new post to obtain post.id
        db.session.add(new_post)
        db.session.commit()
        
        post_tags = request.form.getlist('tag-check')
        
        # loop through all selected tags to get their ids and commit them to db
        for tag in post_tags:
            tag_id = Tag.query.filter_by(name=tag).one()
            
            new_post_tag = PostTag(post_id=new_post.id, tag_id=tag_id.id)
            
            db.session.add(new_post_tag)
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
        tags = Tag.query.all()
        
        return render_template('edit-post.html', post=post, tags=tags)
    
    if request.method == 'POST':
        
        title = request.form['title']
        content = request.form['content']
        
        updated_post = Post.query.get(post_id)
        updated_post.title = title
        updated_post.content = content
        
        db.session.commit()
        
        existing_tags = list()
        
        for obj in updated_post.tags:
            existing_tags.append(obj.name)
        
        # delete all PostTag rows for this specific post
        for tag in existing_tags:
            
            tag_id = Tag.query.filter_by(name=tag).one()
            delete_tag = PostTag.query.get((updated_post.id, tag_id.id))
            db.session.delete(delete_tag)
            
            print(delete_tag)
            print('Delete')
            
            db.session.commit()
        
        
        post_tags = request.form.getlist('tag-check')
        
        # add all selected tags to PostTag for this post
        for tag in post_tags:
            
            tag_id = Tag.query.filter_by(name=tag).one()
            updated_post_tag = PostTag(post_id=updated_post.id, tag_id=tag_id.id)
            
            print('Add')
            
            db.session.add(updated_post_tag)
            db.session.commit()
        
        return redirect(f'/posts/{post_id}')
    
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Deletes a post and redirects back to a user screen.'''
    
    # get post
    post = Post.query.filter_by(id=post_id).one_or_none()
    post_obj = Post.query.filter_by(id=post_id)
    
    # get PostTag rows and delete
    for post_tag in post.tags:
        tag = Tag.query.filter_by(name=post_tag.name).one()
        delete_tag = PostTag.query.get((post.id, tag.id))
        
        print(delete_tag)
        
        db.session.delete(delete_tag)
        
        db.session.commit()
    
    # delete actual post after removing dependencies
    post_obj.delete()
    
    db.session.commit()
    
    return redirect(f'/users')


@app.route('/tags')
def get_tags():
    '''Gets a list of tags from db and displays them.'''
    
    tags = Tag.query.all()
    
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    '''Gets list of posts that tag appears on.'''
    
    tag = Tag.query.get(tag_id)
    
    return render_template('tag-details.html', tag=tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def new_tags():
    '''Displays a form to add a new tag, and saves the new tag information.'''
    
    if request.method == 'GET':
        return render_template('add-tag.html')
    
    if request.method == 'POST':
        
        name = request.form['tag-name']
        
        new_tag = Tag(name=name)
        
        db.session.add(new_tag)
        db.session.commit()
        
        return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    '''Displays tag edit form.'''
    
    if request.method == 'GET':
    
        tag = Tag.query.get(tag_id)
        
        return render_template('edit-tag.html', tag=tag)
    
    if request.method == 'POST':
        
        name = request.form['tag-name']
        
        update_tag = Tag.query.get(tag_id)
        update_tag.name = name
        
        db.session.commit()
         
        return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Deletes tag from db and redirects to tag list'''
    
    tag = Tag.query.filter_by(id=tag_id)
    tag.delete()
    
    db.session.commit()
    
    return redirect('/tags')