from unicodedata import name
from artistry import app, db, bcrypt
from flask import render_template, request, flash, redirect, url_for
from artistry.forms import RegistrationForm, LoginForm, AccountForm, CreatePostForm
from artistry.models import User, Post
import re
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image



@app.route('/')
@app.route('/home')
def home():
    photo_dict = {}
    
    users = User.query.all()
    for user in users:
        photos = []
        for post in user.posts:
            photos.append(post.photo_file)
        photo_dict[user.username] = photos


    return render_template('home.html', photo_dict=photo_dict)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    # if the user already login it will go to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # print('name-{0}\n username-{1}\n email-{2}\npassword-{3}\n confirm_paassword-{4}\ checkbox-{5}'.format(form.name.data, form.username.data, form.email.data, form.password.data, form.confirm_password.data, form.checkterms.data))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, 
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account has been created successfully', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

def eitherEmailNorUsername(string):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, string):
        return string
    else:
        return 'NOT_EMAIL'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        
        emailOrUsername = eitherEmailNorUsername(form.usernameOrEmail.data)

        if emailOrUsername != 'NOT_EMAIL':
            user = User.query.filter_by(email=emailOrUsername).first()
        else:
            user = User.query.filter_by(username=form.usernameOrEmail.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please try with correct username/email and password', 'danger')

    return render_template('login.html', form=form)


# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#************ SAVE PROFILE PICTURE ***************#
def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    profile_pic_name = random_hex + f_ext
    # save the file -> get the project dir -> desired location -> join them &
    #  -> save
    profile_pic_path = os.path.join(app.root_path, 'static/images/profile_pics', profile_pic_name)

    # open the image data
    output_size = (150, 150)
    profile_pic = Image.open(form_picture)
    profile_pic.thumbnail(output_size)
    profile_pic.save(profile_pic_path)
    return profile_pic_name
#*************** END *****************************#

# account
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    user_photos = []
    
    # add all the photo in user_photos
    for post in user_posts:
        user_photos.append(post.photo_file)


    if form.validate_on_submit():
        if form.profile_pic.data:
            profile_picture = save_profile_picture(form.profile_pic.data)
            current_user.image_file = profile_picture

        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
            
    image_file = url_for('static', filename='/images/profile_pics/'+current_user.image_file)

    return render_template('account.html', form=form, profile_image=image_file, current_user=current_user, user_photos=user_photos)


def save_photos(form_picture, username):
    dir_name = 'static\\photos\\'+username+'\\'
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    print(picture_name)
    # check dir
    desired_path = os.path.join(app.root_path, dir_name)
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    photo_path = os.path.join(desired_path, picture_name)

    photo = Image.open(form_picture)
    photo.save(photo_path)
    return picture_name

#_____________ THE POST __________#

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        if form.photo_file.data:
            picture = save_photos(form.photo_file.data, current_user.username)
            print('hii')
        
        # print(form.error)
        post = Post(title=form.title.data, type=form.type.data, photo_file=picture, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post is added', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)




#____________ END POST ____________#