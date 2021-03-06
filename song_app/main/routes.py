from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from song_app.models import Song, Artist, Album, User
from song_app.main.forms import SongForm, ArtistForm, AlbumForm
from song_app import bcrypt

from song_app import app, db

main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def homepage():
    all_songs = Song.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_songs=all_songs, all_users=all_users)

@main.route('/create_song', methods=['GET', 'POST'])
@login_required
def create_song():
    form = SongForm()

    if form.validate_on_submit(): 
        new_song = Song(
            title=form.title.data,
            release_date=form.release_date.data,
            artist=form.artist.data,
            genre=form.genre.data,
            albums=form.albums.data
        )
        db.session.add(new_song)
        db.session.commit()

        flash('New song was created successfully.')
        return redirect(url_for('main.song_info', song_id=new_song.id))
    return render_template('create_song.html', form=form)

@main.route('/create_artist', methods=['GET', 'POST'])
@login_required
def create_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_artist)
        db.session.commit()

        flash('New artist created successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_artist.html', form=form)

@main.route('/create_album', methods=['GET', 'POST'])
@login_required
def create_album():
    form = AlbumForm()
    if form.validate_on_submit():
        new_album = Album(
            name=form.name.data
        )
        db.session.add(new_album)
        db.session.commit()

        flash('New album created successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_album.html', form=form)

@main.route('/song/<song_id>', methods=['GET', 'POST'])
def song_info(song_id):
    song = Song.query.get(song_id)
    form = SongForm(obj=song)

    if form.validate_on_submit():
        song.title = form.title.data
        song.release_date = form.release_date.data
        song.artist = form.artist.data
        song.genre = form.genre.data
        song.albums = form.albums.data

        db.session.commit()

        flash('Song was updated successfully.')
        return redirect(url_for('main.song_info', song_id=song_id))

    return render_template('song_info.html', song=song, form=form)


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)


@main.route('/favorite/<song_id>', methods=['POST'])
@login_required
def favorite_song(song_id):
    song = Song.query.get(song_id)
    if song in current_user.favorite_songs:
        flash('Song is already in favorites.')
    else:
        current_user.favorite_songs.append(song)
        db.session.add(current_user)
        db.session.commit()
        flash('Song added to favorites.')
    return redirect(url_for('main.song_info', song_id=song_id))


@main.route('/unfavorite/<song_id>', methods=['POST'])
@login_required
def unfavorite_book(song_id):
    song = Song.query.get(song_id)
    if song not in current_user.favorite_songs:
        flash('Song not in favorites.')
    else:
        current_user.favorite_songs.remove(song)
        db.session.add(current_user)
        db.session.commit()
        flash('Song removed from favorites.')
    return redirect(url_for('main.song_info', song_id=song_id))