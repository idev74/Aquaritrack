import os
import unittest
import app

from datetime import date
from aquaritrack.extensions import app, db, bcrypt
from aquaritrack.models import *

"""
Run these tests with the command:
python -m unittest aquaritrack.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_items():
    species="Betta Fish"
    quantity=5
    category="FISH"
    photo_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F397000000000000"

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_in(self):
        """Test that the books show up on the homepage."""
        create_items()
        create_user()
        login(self.app, 'me1', 'password')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('To Kill a Mockingbird', response_text)
        self.assertIn('The Bell Jar', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Create Book', response_text)
        self.assertIn('Create Author', response_text)
        self.assertIn('Create Genre', response_text)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_book_detail_logged_out(self):
        """Test that the book appears on its detail page."""
        create_items()
        create_user()
        response = self.app.get('/book/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('<h1>To Kill a Mockingbird</h1>', response_text)
        self.assertIn('Harper Lee', response_text)
        self.assertNotIn('Favorite This Book', response_text)

    def test_book_detail_logged_in(self):
        """Test that the book appears on its detail page."""
        create_items()
        create_user()
        login(self.app, 'me1', 'password')
        response = self.app.get('/book/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('<h1>To Kill a Mockingbird</h1>', response_text)
        self.assertIn('Harper Lee', response_text)
        self.assertIn('Favorite This Book', response_text)

    def test_update_book(self):
        """Test updating a book."""
        create_items()
        create_user()
        login(self.app, 'me1', 'password')
        post_data = {
            'title': 'Tequila Mockingbird',
            'publish_date': '1960-07-12',
            'author': 1,
            'audience': 'CHILDREN',
            'genres': []
        }
        self.app.post('/book/1', data=post_data)
        book = Book.query.get(1)
        self.assertEqual(book.title, 'Tequila Mockingbird')
        self.assertEqual(book.publish_date, date(1960, 7, 12))
        self.assertEqual(book.audience, Audience.CHILDREN)

    def test_create_book(self):
        """Test creating a book."""
        create_items()
        create_user()
        login(self.app, 'me1', 'password')
        post_data = {
            'title': 'Go Set a Watchman',
            'publish_date': '2015-07-14',
            'author': 1,
            'audience': 'ADULT',
            'genres': []
        }
        self.app.post('/create_book', data=post_data)
        created_book = Book.query.filter_by(title='Go Set a Watchman').one()
        self.assertIsNotNone(created_book)
        self.assertEqual(created_book.author.name, 'Harper Lee')

    def test_create_book_logged_out(self):
        """
        Test that the user is redirected when trying to access the create book 
        route if not logged in.
        """
        create_items()
        create_user()
        response = self.app.get('/create_book')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_book', response.location)

    def test_create_author(self):
        """Test creating an author."""
        create_user()
        login(self.app, 'me1', 'password')
        post_data = {
            'name': 'Roald Dahl',
            'biography': 'I write books.'
        }
        self.app.post('/create_author', data=post_data)
        created_author = Author.query.filter_by(name='Roald Dahl').one()
        self.assertIsNotNone(created_author)
        self.assertEqual(created_author.biography, 'I write books.')
