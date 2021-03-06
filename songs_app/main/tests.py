# Create your tests here.
import os
import unittest
from datetime import datetime
from songs_app import app, db, bcrypt
from songs_app.models import User, Genre, Album, Song, Artist

'''
command to run tests: python -m unittest songs_app.main.tests
'''

#setup

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

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

#tests

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

    def test_homepage_logged_out(self):
        """Test that the books show up on the homepage."""
        # Set up
        create_songs()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Tyler Herro', response_text)
        self.assertIn('Epidemic', response_text)
        self.assertIn('omar', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Song', response_text)
        self.assertNotIn('Create Artist', response_text)
        self.assertNotIn('Create Album', response_text)
    
    def test_homepage_logged_in(self):
        """Test that the books show up on the homepage."""
        create_songs()
        create_user()
        login(self.app, 'omar', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Tyler Herro', response_text)
        self.assertIn('Epidemic', response_text)
        self.assertIn('omar', response_text)
        self.assertIn('Create Song', response_text)
        self.assertIn('Create Artist', response_text)
        self.assertIn('Create Album', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)
    
    def test_update_song(self):
        """Test updating a book."""
        create_songs()
        create_user()
        login(self.app, 'omar', 'password')

        post_data = {
            'title': 'The Bigger Picture',
            'release_date': '2020-12-06',
            'artist': 1,
            'genres': 'HIP_HOP',
            'albums': []
        }
        self.app.post('/song/1', data=post_data)

        song = Song.query.get(1)
        self.assertEqual(song.title, 'The Bigger Picture')
        self.assertEqual(song.release_date, date(2020, 12, 6))
        self.assertEqual(song.genre, Genre.HIP_HOP)
    
    def test_profile_page(self):
        create_songs()
        create_user()
        login(self.app, 'omar', 'password')
        db.session.commit()
        response = self.app.get('/profile/omar', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('omar', response_text)

    def test_favorite_song(self):
        create_songs()
        create_user()
        login(self.app, 'omar', 'password')
        post_data = {
            'song_id': '1'
        }
        self.app.post('/favorite/1', data=post_data)
        user = User.query.filter_by(username='omar').one()
        self.assertIsNotNone(user.favorite_books)

    def test_unfavorite_song(self):
        create_songs()
        create_user()
        login(self.app, 'omar', 'password')
        post_data = {
            'song_id': '1'
        }
        self.app.post('/favorite/1', data=post_data)
        self.app.post('/unfavorite/1', data=post_data)
        user = User.query.filter_by(username='omar').one()
        self.assertEqual(user.favorite_songs, [])