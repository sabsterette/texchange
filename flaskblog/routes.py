import secrets
import os
#needs Pillow to resize images
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
# render_template allows returning of files,
# flash allows to send flash messagees
from flaskblog.forms import RegistrationForm, LoginForm, CreateForm, CreateReview, \
 SearchForm, editItemForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post, Reviews 
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask
from flask_mail import Mail, Message

@app.route("/", methods=['GET', 'POST'])
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
            flash(f'Welcome Back {user.username}!', 'label')
            #turnary conditional
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('log in unsuccessful, try again', 'help-block')
    return render_template('login.html', title='Login', form=form)

@app.route("/home", methods=['GET'])
@login_required
def home():
    posts = current_user.posts
    return render_template('home.html', posts=posts)



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



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

# def save_picture(form_picture):
#     #saving the name of the picture as a random sequence
#     random_hex = secrets.token_hex(8)
#     #this saves the file name as well as the extention
#     #allows us to remember the extention, we only need to remember the extention
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     #gives the full path all the way to the static directory
#     picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
#     #Resizes file to make sure the pictures do not take up too much space
#     output_size=(125, 125)
#     i=Image.open(form_picture)
#     i.thumbnail(output_size)

#     i.save(picture_path)
#     return picture_fn

@app.route("/profile/<userprofile>", methods=['GET'])
@login_required
def profile(userprofile):
    user=User.query.filter_by(username=userprofile).first()
    reviews=user.reviews
    ratings=0
    if reviews:
        for review in reviews:
            ratings=ratings+review.rating
        avg_rating=ratings/len(reviews)
    else:
        avg_rating=None 
    return render_template('profile.html', title='PROFILE', user=user, reviews=reviews,
    avg_rating=avg_rating)


@app.route("/review/<userprofile>", methods=['GET', 'POST'])
@login_required
def review(userprofile):                                                      
    user = User.query.filter_by(username=userprofile).first()                  
    form = CreateReview()
    if form.validate_on_submit():
        if form.anonymous.data == True: 
            review=Reviews(rating=int(form.rating.data, 10), description=form.description.data, 
            user_id=user.id, reviewer=None)
        else:
            review=Reviews(rating=int(form.rating.data, 10), description=form.description.data, 
            user_id=user.id, reviewer=current_user.username)
        db.session.add(review)
        db.session.commit()
        flash(f'You have created a review for {userprofile}!', 'success')
        return redirect(url_for('profile', userprofile=userprofile))
    return render_template('review.html', form=form)

# @app.route("/edit-profile", methods=['GET', 'POST'])
# @login_required
# def editAccount():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file=save_picture(form.picture.data)
#             current_user.image_file=picture_file
#         current_user.username=form.username.data
#         current_user.email=form.email.data
#         db.session.commit()
#         flash('Account is updated.', 'label')
#         return redirect(url_for('account'))
#     elif request.method=='GET':
#         form.username.data=current_user.username
#         form.email.data=current_user.email
#     #assigns the profile pic to the one uploaded by user
#     image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
#     #pass in all the required data for getting the profile
#     return render_template('profile.html', title='PROFILE', image_file=image_file, form=form)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    searchForm = SearchForm()
    message = "Search for a textbook!"
    posts=Post.query.all()
    users=User.query.all()
    if searchForm.validate_on_submit():
        message=""
        return results(searchForm)
    return render_template('search.html', title='Search', form=searchForm,
    message=message, posts=posts)

#function used for searching and retrieving posts
#All the if statements are used for getting the post to be sort by a certain property
#Uses post.query.filter and post.query.order_by from flask sqlalchemy
@app.route("/results", methods=['GET', 'POST'])
def results(searchForm):
    #uses a list results to store the posts
    results=[]
    users=User.query.all()
    if searchForm.sort_by.data == 'price':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).order_by(Post.price).all()
    if searchForm.sort_by.data == 'classid':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).order_by(Post.class_id).all()
    if searchForm.sort_by.data == 'condition':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).order_by(Post.quality).all()
    if searchForm.sort_by.data == 'date':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).order_by(Post.date_posted).all()
    if searchForm.sort_by.data == 'edition':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).order_by(Post.edition).all()
    if searchForm.sort_by.data == 'select one':
        results=Post.query.filter(Post.title.like('%'+searchForm.title.data+'%'),
        Post.authors.like('%'+searchForm.authors.data+'%')).all()
    if results:
        message=f'Showing search results for {searchForm.title.data} {searchForm.authors.data}'
        return render_template('search.html', title='Search Results', form=searchForm,
         message=message, posts=results)
    else:
        flash('No Search Results Found', 'fail')
        return render_template('search.html', title='Search Results', form=searchForm,
         posts=results)

#Post.class_id.like('%'+searchForm.class_id.data+'%')


@app.route("/create", methods=['GET', 'POST'])
@login_required
def createItem():
    form = CreateForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, edition=form.edition.data, authors=form.authors.data,
        price=form.price.data, user_id=current_user.id, class_id=form.course.data,
        quality=form.quality.data, description=form.description.data)
        db.session.add(post)
        db.session.commit()
        flash('Your item has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', title='Create Listing', form=form)

@app.route("/items/<post_id>")
def items(post_id):
    post=Post.query.get(post_id)
    user=User.query.get(post.user_id)
    return render_template('items.html', post=post, user=user)

@app.route("/editItem/<post_id>", methods=['GET', 'POST'])
def editItem(post_id):
    post=Post.query.get(post_id)
    user=User.query.get(post.user_id)
    form=editItemForm()
    #update information if need to
    if form.validate_on_submit():
        post.title=form.title.data
        post.edition=form.edition.data
        post.authors=form.authors.data
        post.price=form.price.data
        post.class_id=form.course.data
        post.quality=form.quality.data
        post.description=form.description.data
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('home'))
    #else display the information
    elif request.method=='GET':
        form.title.data=post.title
        form.edition.data=post.edition
        form.authors.data=post.authors
        form.price.data=post.price
        form.course.data=post.class_id
        form.quality.data=post.quality
        form.description.data=post.description
    return render_template('edit-item.html', form=form, post=post, user=user)

# Delete Listing
@app.route("/delete_listing/<post_id>", methods=['POST'])
@login_required
def delete_listing(post_id):
   # Create delete_this
   delete_this = Post.query.get(post_id)
   # Delete listing
   db.session.delete(delete_this)
   # Commit to db
   db.session.commit()
   # Flash message to alert user
   flash('This listing has been deleted', 'success')
   return redirect(url_for('home'))

# configure settings to send email from gmail
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'texchange.cwru@gmail.com',
    "MAIL_PASSWORD": 'cwru1234'
}
app.config.update(mail_settings)
mail = Mail(app)

# Send email to user who posted listing
@app.route("/sendEmail/<user_email>/<current_user_email>", methods=['GET', 'POST'])
def sendEmail(user_email, current_user_email):
    # get email to send to
    user=User.query.get(user_email)
    # get current user email to inform poster of who is interested
    current_user=User.query.get(current_user_email)
    msg = Message(subject="[Texchange] Listing Information Request",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[user_email],
                      body='Hello!\n Someone has requested more information about your listing. You can contact them at '+current_user_email+'.\n Thanks for using Texchange!')
    mail.send(msg)
    flash('The email has been sent! The poster will be in contact shortly.', 'success')
    return redirect(url_for('search'))
