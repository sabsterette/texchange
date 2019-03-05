from flask import Flask, render_template, url_for, flash, redirect
# render_template allows returning of files,
# flash allows to send flash messagees
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '8d5eb5a677fc571260474b96e559afd5'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


#class User(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(80), unique=True, nullable=False)
 #   email = db.Column(db.String(120), unique=True, nullable=False)
  #  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
   # password = db.Column(db.String(60), nullable=False)


    #def __repr__(self):
      #  return f"user('{self.username}')"




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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created or {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('log in unsuccessful, try again', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
