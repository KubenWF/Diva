from app import db
from .association_tables import user_albums,list_albums
import json

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    billboard = db.Column(db.String(120), nullable=True)
    artists = db.Column(db.String(255), nullable=True)
    total_tracks = db.Column(db.Integer, nullable=True)
    album_type = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    
    albums_users = db.relationship('User', secondary=user_albums, backref=db.backref('saved_users', lazy='dynamic'))

    # featured_artists = db.relationship('Artist', secondary=album_artists, backref=db.backref('albums_included', lazy='dynamic'))
    # genres = db.relationship('Genre', secondary=album_genres, backref=db.backref('albums_genres', lazy='dynamic'))

    def to_json(self):
        return {
            "album_id": self.id,
            "name": self.name,
            "billboard": self.billboard if self.billboard else None,
            "artists":self.artists,
            "total_tracks":self.total_tracks,
            "albums_users": [{"album_id": user.id} for user in self.albums_users],
            "album_type":self.album_type,
            "image_url":self.image_url
        }
    
    def __repr__(self):
        return f" Album ID: {self.id}. Album name: {self.name}. Album Users: {[user.to_json() for user in self.albums_users]}"