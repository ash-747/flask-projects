#random thoughts & notes for my own records (or anyone that needed it)

#when done go to python --> from dynamicexample3 import db --> db.create_all() 
#from there you will have a created a db file b/c you're using a SQLite file
#to import current models --> from dynamicexample3 import User, Post
#now you can test to see how everything is working i.e. user_1 = User(username='Ash', email='A@gmail.com', password='password') 
#^id will be assigned automatically, since we did not assign a key then --> add user to database by db.session.add(user_1) --> db.session.commit() to commit to the db

#to get query of all users use User.query.all() i.e. User('Ash', 'A@gmail.com', 'default.jpg') or you access specific first User by User.query.first()
#you can also filter by User.query.filter_by(insert w/e).all
#or give a variable like user = User.query.filter_by(username='Ash').first() --> then put int user | now you can play around w/ additional attributes i.e. put in user.id and get 1 
#or play around with user = User.query.get(1) --> get same result as user

#check this person's posts by user.posts --> create post by i.e. post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)

#notes on user authentication and passwords: 
#pip install flask-bcrypt, bcrypt is really cool for hashing then python interpreter 
# --> from flask_bcrypt import Bcrypt --> bcrypt = Bcrypt() 
# --> bcrypt.generate_password_hash('testing') to hash a password --> from there you can decode by bcrypt.generate_password_hash('testing').decode('utf-8')
#to check if passwords are equal go to hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8') --> bcrypt.check_password_hash(hashed_pw, 'yourpassword')

#after you have created the password you can now play around with the register route then when you are done get out of the server and 
#go to interpreter --> from dynamicexample3 import db --> from dynamicexample3.models import User --> user = User.query.first() --> user --> user.password to see all of your logins and hashed passwords
#after properly preventer duplicate accounts in forms now - registration system

#time to make a login system through flask login --> pip install flask-login --> init file -->

#sidenote: you don't want to be in debug when app is deployed

#Pillow module in Flask allows you to resize images. Install by --> pip install Pillow
#You resize images because larger images can make the site run slower 
