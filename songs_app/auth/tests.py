# Create your tests here.
import os
import unittest
from datetime import date
from songs_app import app, db, bcrypt
from songs_app.models import Song, Artist, Album, User, Genre

"""
Run these tests with the command:
python -m unittest songs_app.main.tests
"""

#################################################
# Setup
#################################################

def create_songs():
    a1 = Artist(name='Jack Harlow')
    b1 = Song(
        title='Tyler Herro',
        release_date=date(2020-10-22),
        artist=a1
    )
    db.session.add(b1)

    a2 = Artist(name='Polo G')
    b2 = Song(
        title='Epidemic',
        release_date=date(2020-10-25),
        artist=a2
        )
    db.session.add(b2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='omar', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(unittest.TestCase):
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
        """Tests to check if the created user exists in database"""
        post_data = {
            'username' : 'omarlopez',
            'password' : 'lopez2001'
        }
        self.app.post('/signup', data=post_data)
        new_user = User.query.filter_by(username='omarlopez').one()
        self.assertIsNotNone(new_user)

    def test_signup_existing_user(self):
        """Tests to make sure username is not taken"""
        post_data = {
            'username' : 'omarlopez',
            'password' : 'lopez2001'
        }
        self.app.post('/signup', data=post_data)
        response = self.app.post('/signup', data=post_data)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please insert another one.', response_text)

    def test_login_correct_password(self):
        """Tests that login button disappears from homepage after a successful login"""
        post_data = {
            'username' : 'omarlopez',
            'password' : 'lopez2001'
        }
        self.app.post('/signup', data=post_data)
        response = self.app.post('/login', data=post_data)
        response_text = (self.app.get('/', follow_redirects=True)).get_data(as_text=True)
        self.assertNotIn('Login', response_text)

    def test_login_nonexistent_user(self):
        """Tests to make sure a nonexistent user cannot log in"""
        post_data = {
            'username' : 'notuser',
            'password' : 'notpassword'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Username does not exist. Please try again.', response_text)

    def test_login_incorrect_password(self):
        """Tests that the correct form is displayed when an incorrect password is used"""
        post_data = {
            'username' : 'omarlopez',
            'password' : 'lopez2001'
        }
        self.app.post('/signup', data=post_data)
        post_data = {
            'username' : 'omarlopez',
            'password' : 'incorrectpassword'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Password does not match. Please try again.', response_text)

    def test_logout(self):
        """Tests that user can logout and login button appears on homepage"""
        post_data = {
            'username' : 'omarlopez',
            'password' : 'lopez2001'
        }
        self.app.post('/signup', data=post_data)
        self.app.post('/login', data=post_data)
        response = self.app.post('/logout', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)