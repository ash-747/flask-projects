import os
import secrets
from PIL import Image #PIL was installed when we installed Pillow pkg
from flask import render_template, url_for, flash, redirect, request, abort
from dynamicexample3 import app, db, bcrypt
from dynamicexample3.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from dynamicexample3.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #to check db pw matches    
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #args is dictionary, if get doesn't exist then it will return none
            return redirect(next_page) if next_page else redirect(url_for('home')) #terinary conditional
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger') #danger is bootstrap equivalent to 'failure'
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture): 
    random_hex = secrets.token_hex(8) #randomizing name of image but import secrets, cause you don't want same name of picture, 
    #make sure you're save it with same file as was mentions so import os | returns file name w/o ext, then returns ext itself
    _, f_ext = os.path.splitext(form_picture.filename) #not using f_name at all, just using extention, so in python you can just use an _
    picture_fn = random_hex + f_ext #fn = filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #using os.path.join makes sure image is properly concatenated in one long path
    
    #simple example of pillow resizing
    #output_size = (250, 250)
    #i = Image.open(form_picture)
    #i.thumbnail(output_size)
    #i.save(picture_path)
    
    form_picture.save(picture_path) #how we'll save the image by calling form_picture, the argument, picture_path, is where we'll save it
    #this function is just about our saving our image so far so user can create image outside this function so we just put a return
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required #now extention knows that we need to login to access this route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: #code to save user profile pic is logically its own function, see save_picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

#creating a variable where the id of the post is part of the route 
#making a route that take us to specific route for a specific host
#flask gives us ability to add variables to our routes
#for example now the user can go to /post/1, /post/2, etc. You can also specify string or integer instead of post_id for example
@app.route("/post/<post_id>")
def post(post_id):
    #get_or_404 means give me a post w/ this id and if it doesn't exist return a 404 (page doesn't exist)
    post = Post.query.get_or_404(post_id) #remember when we getting something by an id we can use the get method
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 is http response for a forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST']) #only accepting post requests through modal
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post) #after post is deleted we can now redirect them back to home page
    db.session.commit() #notice that we don't have to add since this is already in the database
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


