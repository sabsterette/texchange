import secrets
import os
#needs Pillow to resize images
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
# render_template allows returning of files,
# flash allows to send flash messagees
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey',
        'title': 'Mine',
        'content': 'Fun',
        'date_posted': 'today'
    },
    {
        'author': 'Me',
        'title': 'WOOT',
        'content': 'No',
        'date_posted': 'Yesterday'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    #validate_on_submit won't catch duplicates even though models say it has to be unique
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #gets the page they were trying to access
            flash(f'Welcome Back {user.username}!', 'success')
            #turnary conditional
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('log in unsuccessful, try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    #saving the name of the picture as a random sequence
    random_hex = secrets.token_hex(8)
    #this saves the file name as well as the extention
    #allows us to remember the extention, we only need to remember the extention
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #gives the full path all the way to the static directory
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    #Resizes file to make sure the pictures do not take up too much space 
    output_size=(125, 125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account is updated.', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    #assigns the profile pic to the one uploaded by user
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    #pass in all the required data for getting the profile
    return render_template('account.html', title='Account', image_file=image_file, form=form)