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
        assert b'Welcome testing!' in response.data
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

    def editUser(self, userprofile, username, email, bio):
        return self.app.post(f'/editProfile/{userprofile}', data=dict(username=username,
        email=email, bio=bio), follow_redirects=True)

    def test_editUser(self):
        self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        self.login('testing@gmail.com', 'testing')
        response=self.editUser('testing', 'testing', 'testing@gmail.com', 'This is my bio')
        user=User.query.first()
        bio='This is my bio'
        self.assertEqual(bio, user.bio)
        assert b'Your profile has been updated!' in response.data
        self.logout()
        #try with another user to make sure username can't be changed 
        self.register('tester', 'tester@gmail.com', 'testing', 'testing')
        self.login('tester@gmail.com', 'testing')
        response=self.editUser('tester', 'testing', 'tester@gmail.com', '')
        assert b'Oops! Username already taken!' in response.data
        #test for email that already exists
        response=self.editUser('tester', 'tester', 'testing@gmail.com', '')
        assert b'Oops! That email is already linked to an account!' in response.data
        # test for correct username change
        response=self.editUser('tester', 'tested', 'tester@gmail.com', '')
        assert b'Your profile has been updated!' in response.data
        user=User.query.filter_by(username='tested').first()
        self.assertEqual(user.username, 'tested')
        # test for correct email change
        response=self.editUser('tested', 'tested', 'tested@gmail.com', '')
        assert b'Your profile has been updated!' in response.data
        user=User.query.filter_by(username='tested').first()
        self.assertEqual(user.email, 'tested@gmail.com')

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
    def createReview(self, userprofile, rating, description, anonymous):
        return self.app.post(f'/review/{userprofile}', data=dict(rating=rating, description=description,
        anonymous=anonymous), follow_redirects=True)

    def test_createReview(self):
        # user that will be reviewed
        self.register('reviewee', 'testing@gmail.com', 'testing', 'testing')
        # user that will be reviewing
        self.register('reviewing', 'reviewer@gmail.com', 'testing', 'testing')
        self.login('reviewer@gmail.com', 'testing')
        response=self.createReview('reviewee', '3', 'responded very quickly', True)
        user=User.query.filter_by(username='reviewee').first()
        rev="[Reviews('3', 'responded very quickly')]"
        #test that the review is in the user reviews 
        self.assertEqual(rev, f"{user.reviews}")
        #make sure the post is anonymous
        assert b'Anonymous' in response.data
        response=self.createReview('reviewee', '5', '', None)
        #reassign user to update the number of reviews
        user=User.query.filter_by(username='reviewee').first()
        rev1="[Reviews('3', 'responded very quickly'), Reviews('5', '')]"
        self.assertEqual(rev1, f"{user.reviews}")
        #make sure the post is not anonymous
        assert b'reviewing' in response.data
        # see if the average rating is correct
        assert b'4.0' in response.data


    ##########################################################
    ################# TEST FOR SEARCHING #####################
    ##########################################################
    def search(self, title, authors, sort_by):
        # the sort_by was tested manually, needed to be included for the tests to work
        return self.app.post('/search', data=dict(title=title, authors=authors, sort_by=sort_by), 
        follow_redirects=True)

    def test_search(self):
        self.register('testing', 'testing@gmail.com', 'testing', 'testing')
        self.login('testing@gmail.com', 'testing')
        self.create('Math', '2', 'Professor', '9.00', 'Math 201', 'Brand New', 'good textbook')
        self.create('Movies', '3', 'Melvin', '14.00', 'Film 201', 'Brand New', 'Unhelpful')
        self.create('Business & Management', '4', 'Melvin', '30.00', 'Bman 201', 'Brand New', 'useful textbook')
        response=self.search('', '', 'price')
        #check that all the textbooks appear in the search
        assert b'Movies' in response.data
        assert b'Math' in response.data
        #&amp; needs to be used to check for & in the HTML response
        assert b'Business &amp; Management' in response.data
        #search by just using title
        response=self.search('Math', '', 'price')
        # make sure that only the textbook with title Math is in the result
        assert b'Movies' not in response.data
        assert b'Math' in response.data
        assert b'Business &amp; Management' not in response.data
        #search by just using author
        response=self.search('', 'Melvin', 'price')
        # only textbooks with Melvin as authors should appear
        assert b'Movies' in response.data
        assert b'Math' not in response.data
        assert b'Business &amp; Management' in response.data
        # search by both title and author
        response=self.search('Movies', 'Melvin', 'price')
        # only textbook with matching title and author 
        assert b'Movies' in response.data
        assert b'Math' not in response.data
        assert b'Business &amp; Management' not in response.data


if __name__ == "__main__":
    unittest.main()