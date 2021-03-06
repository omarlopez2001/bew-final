# Create your models here.
from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Genre(FormEnum):
    HIP_HOP = 'Hip-Hop'
    POP = 'Pop'
    ROCK = 'Rock'
    OTHER = 'Other'

class Song(db.Model):
    """Song model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Date)

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', back_populates='songs')

    genre = db.Column(db.Enum(Genre), default=Genre.ALL)

    albums = db.relationship(
        'Album', secondary='song_album', back_populates='songs')

    user_favorite_songs = db.relationship(
        'User', secondary='user_song', back_populates='favorite_songs')

    def __str__(self):
        return f'<Song: {self.title}>'

    def __repr__(self):
        return f'<Song: {self.title}>'

class Artist(db.Model):
    """Artist model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    songs = db.relationship('Song', back_populates='artist')

    def __str__(self):
        return f'<Artist: {self.name}>'

    def __repr__(self):
        return f'<Artist: {self.name}>'

class Album(db.Model):
    """Album model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    songs = db.relationship(
        'Song', secondary='song_album', back_populates='albums')

    def __str__(self):
        return f'<Album: {self.name}>'

    def __repr__(self):
        return f'<Album: {self.name}>'

song_album_table = db.Table('song_album',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_songs = db.relationship(
        'Song', secondary='user_song', back_populates='user_favorite_songs')

    def __repr__(self):
        return f'<User: {self.username}>'

favorite_songs_table = db.Table('user_song',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)