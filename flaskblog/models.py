from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

# Signs in to the user_id's account by querying the User table.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# This is the model for the table "User" which holds the data relevant for users.
# Required attributes are referenced by "nullable=False"
# The User model is a stand-in for the table and temporarily stores values in the
#   form of the database table and adds its data to the .db file when db.session.add(foo)
#   is called then commits it when db.session.commit() is called where foo is the
#   instance of the User class/model.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)
    reviews = db.relationship('Reviews', backref='reviewee', lazy=True)

    #repr is basically toString
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# This is the model for the table "Post" which holds the data relevant for posts.
# Required attributes are referenced by "nullable=False"
# The Post model is a stand-in for the table and temporarily stores values in the
#   form of the database table and adds its data to the .db file when db.session.add(foo)
#   is called then commits it when db.session.commit() is called where foo is the
#   instance of the Post class/model.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quality = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.String(7), nullable=False)
    edition = db.Column(db.Integer)

    def __repr__(self):
        return f"Post('{self.title}', '{self.price}')"

# This is the model for the table "Reviews" which holds the data relevant for reviews.
# Required attributes are referenced by "nullable=False"
# The Reviews model is a stand-in for the table and temporarily stores values in the
#   form of the database table and adds its data to the .db file when db.session.add(foo)
#   is called then commits it when db.session.commit() is called where foo is the
#   instance of the Reviews class/model.
class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

    #repr is basically toString
    def __repr__(self):
        return f"Reviews('{self.rating}', '{self.description}')"
