import os
import unittest
import tempfile
 
from flask_login import current_user
from flaskblog import app, db
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm

TEST_DB = 'test.db'
 
class FlaskblogTests(unittest.TestCase):

    #setting up a new test database 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
    #tear down what was previously set up 
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ##########################################################
    #################### TEST FOR USERS ######################
    ##########################################################
    def register(self, username, email, password, confirm_password):
        return self.app.post('/register', data=dict(username=username, email=email,
        password=password, confirm_password=confirm_password), follow_redirects=True)
    
    def test_register(self):
        response=self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        #testing the message that's sent
        assert b'Your account has been created!' in response.data
        #test that the database now has this user
        #this is the first item in the database so the id number is 1
        u="User('testing', 'testing@gmail.com')"
        self.assertEqual(f"{User.query.get(1)}", u)
        #try registering with the same username, should fail
        response=self.register('testing', 'tester@gmail.com', 'testing', 'testing')
        assert b'Username already taken oops!' in response.data
        #it should not have been added into the database so id 2 is empty 
        self.assertEqual(User.query.get(2), None)
        #try registering with the same email, should fail
        response=self.register('tester', 'testing@gmail.com', 'testing', 'testing')
        assert b'Email already taken oops!' in response.data
        self.assertEqual(User.query.get(2), None)
        #passwords do not match, should fail
        response=self.register('tester', 'tester@gmail.com', 'testing', 'tester')
        assert b'Field must be equal to password.' in response.data
        self.assertEqual(User.query.get(2), None)
        #add another successful registration
        response=self.register('tester', 'tester@gmail.com', 'tester', 'tester')
        assert b'Your account has been created!' in response.data
        u="User('tester', 'tester@gmail.com')"
        self.assertEqual(f"{User.query.get(2)}", u)

    #function to use the login form 
    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email,
        password=password), follow_redirects=True)

    #function to log out of the app
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def test_login_logout(self):
        #create some users to test login
        self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        response=self.login('testing@gmail.com', 'testing')
        assert b'Welcome Back testing!' in response.data
        response=self.logout()
        assert b'You have been logged out' in response.data
        #testing using the wrong password
        response=self.login('testing@gmail.com', 'tester')
        assert b'log in unsuccessful, try again' in response.data
        #testing using the wrong email
        response=self.login('tester@gmail.com', 'testing')
        assert b'log in unsuccessful, try again' in response.data
    
    ##########################################################
    ################ TEST FOR EDITING USERS ##################
    ##########################################################

    ##########################################################
    ################ TEST FOR CREATING ITEMS #################
    ##########################################################

    #creating a listing 
    def create(self, title, edition, authors, price, course, quality, description):
        return self.app.post('/create', data=dict(title=title, edition=edition, 
        authors=authors, price=price, course=course, 
        quality=quality, description=description), follow_redirects=True)

    def test_create(self):
        #create user and log in to test creating a listing
        self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        self.login('testing@gmail.com', 'testing')
        u=User.query.get(1)
        response=self.create('Math', '2', 'Professor', '9.00', 'Math 201', 'Brand New', 'good textbook')
        p="Post('Math', '9.0')"
        #check if it is in the database 
        self.assertEqual(f"{Post.query.get(1)}", p)
        self.logout()
        #ensuring that 2 different accounts will post to the same database
        self.register('tester', 'tester@gmail.com', 'tester', 'tester')
        self.login('tester@gmail.com', 'tester')
        u=User.query.get(1)
        response=self.create('Functions', '23', 'John', '10.00', 'Math 202', 'Brand New', 'Useful')
        p="Post('Functions', '10.0')"
        #check if it is in the database as the second item overall
        self.assertEqual(f"{Post.query.get(2)}", p)
        self.logout()
        #make sure they have to log in to make a post
        response=self.create('Movies', '3', 'Melvin', '14.00', 'Film 201', 'Brand New', 'Unhelpful')
        assert b'Please log in to access this page.' in response.data
        self.assertEqual(User.query.get(3), None)

    ##########################################################
    ################ TEST FOR EDITING ITEMS ##################
    ##########################################################
    def editItem(self, post_id, title, edition, authors, price, course, quality, description):
        #the post_id specifies the item to edit 
        return self.app.post(f'/editItem/{post_id}', data=dict(title=title, edition=edition, 
            authors=authors, price=price, course=course, 
            quality=quality, description=description), follow_redirects=True)
    
    def test_editItems(self): 
        self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        self.login('testing@gmail.com', 'testing')
        self.create('Math', '2', 'Professor', '9.00', 'Math 201', 'Brand New', 'good textbook')
        #now modify the item that was created before and see if the correct
        #parts were modified and the others stayed the same
        self.editItem(1, 'Mathematics', '2', 
        'Professor', '30.0', 'Math 201', 'Lightly Used', 'good textbook')
        p="Post('Mathematics', '30.0')"
        self.assertEqual(f'{Post.query.get(1)}', p)
        self.create('Movies', '3', 'Melvin', '14.00', 'Film 201', 'Brand New', 'Unhelpful')
        self.editItem(2, 'Movies', '3', 
        'Melvin', '14.00', 'Film 201', 'Lightly Used', 'Unhelpful')
        p="Post('Movies', '14.0')"
        self.assertEqual(f'{Post.query.get(2)}', p)
        self.assertEqual(Post.query.get(2).quality, 'Lightly Used')

    ##########################################################
    ############## TEST FOR CREATING REVIEWS #################
    ##########################################################

    ##########################################################
    ################# TEST FOR SEARCHING #####################
    ##########################################################
    def search(self, title, authors):
        return self.app.post('/search', data=dict(title=title, authors=authors), 
        follow_redirects=True)

if __name__ == "__main__":
    unittest.main()