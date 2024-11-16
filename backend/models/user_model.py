from app import db
from .association_tables import user_albums
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(80),unique = False, nullable=False) # First name of the user
    last_name = db.Column(db.String(80),unique = False, nullable=False) # Last name of the user
    email = db.Column(db.String(120),unique = True, nullable=False) # Email of the user
    birth_day = db.Column(db.Integer, nullable=False)  # Day of birth
    birth_month = db.Column(db.Integer, nullable=False)  # Month of birth
    birth_year = db.Column(db.Integer, nullable=False)   # Date of birth of the user
    bio = db.Column(db.Text, nullable=True)         # Bio of user

    # favorite_artists = db.relationship('Artist', secondary=favorite_artists, backref=db.backref('artists_users', lazy='dynamic'))
    
    user_albums = db.relationship('Album', secondary=user_albums, backref=db.backref('saved_albums', lazy='dynamic'))

    # owned_lists = db.relationship('List', backref='owner', lazy=True)

    # followed_lists = db.relationship('List', secondary=list_followers, backref=db.backref('lists_followed', lazy='dynamic'))

    # reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def to_json(self):
        birth_date = datetime(self.birth_year, self.birth_month, self.birth_day) if self.birth_day and self.birth_month and self.birth_year else None

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "birth_day": self.birth_day,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "birth_date": birth_date.isoformat() if birth_date else None,
            "bio": self.bio,
            "user_albums": [album.to_json() for album in self.user_albums]
        }

    def __repr__(self):
        return f" User ID: {self.id}. User name: {self.first_name}. User Surname: {self.last_name}"
