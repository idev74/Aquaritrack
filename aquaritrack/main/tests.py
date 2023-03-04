import os
import unittest
import app

from aquaritrack.extensions import app, db, bcrypt
from aquaritrack.models import *

"""
Run these tests with the command:
python3 -m unittest aquaritrack.main.tests
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

def create_tanks():
    t1 = Tank(
        name='My Tank', 
        gallons=10, 
        substrate='GRAVEL', 
        filtration='NONE',
        )
    db.session.add(t1)
    db.session.commit()

    i1 = Item(species='Betta Fish', quantity=1, tank_id=1)

    Tank.query.get(1).items.append(i1)
    db.session.commit()

    t2 = Tank(name='Walstad', gallons=14, substrate='AQUA', filtration='NONE')
    db.session.add(t2)
    db.session.commit()
    
    i2 = Item(species='Cherry Shrimp', quantity=10, tank_id=2)
   
    Tank.query.get(2).items.append(i2)
    db.session.commit()


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
        """Test that the tanks show up on the homepage."""
        create_tanks()
        create_user()
        login(self.app, 'me1', 'password')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('My Tank', response_text)
        self.assertIn('Walstad', response_text)
        self.assertIn('New Tank', response_text)
        self.assertIn('New Item', response_text)
        self.assertIn('Log in', response_text)
        self.assertIn('Sign up', response_text)

    
    def test_create_tank(self):
        """Test creating a tank."""
        create_tanks()
        create_user()
        login(self.app, 'me1', 'password')
        post_data = {
            'name': 'Walstad Tank',
            'gallons': '14',
            'substrate': 'Aqua Soil',
            'filtration': 'None',
        }
        self.app.post('/new_tank', data=post_data)
        created_tank = Tank.query.filter_by(name='Walstad').one()
        self.assertIsNotNone(created_tank)
        self.assertEqual(created_tank.gallons, 14)

    def test_tank_detail(self):
        """Test that the tank appears on its detail page."""
        create_tanks()
        create_user()
        login(self.app, 'me1', 'password')
        tank = Tank.query.get(1)
        response = self.app.get('/tank/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('<h1>Tank - My Tank</h1>', response_text)
        self.assertIn('Gravel', response_text)
        self.assertEqual(tank.gallons, 10)
        self.assertIn('None', response_text)

    def test_update_tank(self):
        """Test updating a tank."""
        create_tanks()
        create_user()
        login(self.app, 'me1', 'password')
        post_data = {
            'name': 'Paradise',
            'gallons': 50,
            'substrate': 'PEAT',
            'filtration': 'OTHER',
        }
        self.app.post('/tank/1', data=post_data)
        tank = Tank.query.get(1)
        self.assertEqual(tank.name, 'Paradise')
        self.assertEqual(tank.gallons, 50)
        self.assertEqual(tank.substrate, SubstrateType.PEAT)
        self.assertEqual(tank.filtration, FilterType.OTHER)