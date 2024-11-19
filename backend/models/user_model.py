from app import db
from flask_login import UserMixin
from .association_tables import user_albums,owner_users_lists
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True) # ID
    user_name = db.Column(db.String(80),unique = True, nullable=False) # User name
    email = db.Column(db.String(120),unique = True, nullable=False) # Email of the user
    password = db.Column(db.String(80), nullable=False) # Password
    birth_day = db.Column(db.Integer, nullable=True)  # Day of birth
    birth_month = db.Column(db.Integer, nullable=True)  # Month of birth
    birth_year = db.Column(db.Integer, nullable=True)   # Date of birth of the user
    bio = db.Column(db.Text, nullable=True)         # Bio of user
    
    # favorite_artists = db.relationship('Artist', secondary=favorite_artists, backref=db.backref('artists_users', lazy='dynamic'))
                
    user_albums = db.relationship('Album', secondary=user_albums, backref=db.backref('saved_albums', lazy='dynamic'))

    owned_lists = db.relationship('List',secondary=owner_users_lists,backref=db.backref('ownerslists', lazy='dynamic'))

    # followed_lists = db.relationship('List', secondary=list_followers, backref=db.backref('lists_followed', lazy='dynamic'))

    # reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password,
            "birth_day": self.birth_day,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "bio": self.bio,
            "user_albums": [{"album_id": album.id} for album in self.user_albums],
            "owned_lists": [{"list_id": list.id} for list in self.owned_lists]
        }

    def __repr__(self):
        return f" User ID: {self.id}. User name: {self.user_name}"
