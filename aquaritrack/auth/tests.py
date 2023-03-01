import app
from unittest import TestCase
from aquaritrack.models import db, User
from aquaritrack.extensions import bcrypt, app, db

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            'username': 'Helloworld',
            'password': 'password'
        }
        self.app.post('/signup', data=post_data)

        response = self.app.get('/profile/Helloworld')
        response_text = response.get_data(as_text=True)
        self.assertIsNotNone('Helloworld', response_text)

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('An account with that username already exists.', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'turtlelover22',
            'password': 'turtles'
        }

        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That user does not exist. Please try again.', response_text)

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'bassword'
        }
        
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('Your username or password is incorrect. Please try again.', response_text)

    def test_logout(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        
        self.app.post('/login', data=post_data)
        self.app.get('/logout')
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)
