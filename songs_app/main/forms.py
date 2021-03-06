# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from songs_app.models import Genre, Song, Artist, Album, User

class SongForm(FlaskForm):
    """Form to create a song"""
    title = StringField('Song Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    release_date = DateField('Release Date')
    artist = QuerySelectField('Artist',
        query_factory=lambda: Artist.query, allow_blank=False)
    genre = SelectField('Genre', choices=Genre.choices())
    albums = QuerySelectMultipleField('Albums',
        query_factory=lambda: Album.query)
    submit = SubmitField('Submit')

class ArtistForm(FlaskForm):
    """Form to create an artist"""
    name = StringField('Artist Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('Artist description')
    submit = SubmitField('Submit')

class AlbumForm(FlaskForm):
    """Form to create an album"""
    name = StringField('Album Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')