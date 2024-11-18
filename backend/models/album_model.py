from app import db
from .association_tables import user_albums,list_albums
import json

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    release_date = db.Column(db.Date, nullable=True)  # Optional field for release date
    cover_art = db.Column(db.String(255), nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    descriptors = db.Column(db.Text, nullable=True)
    

    albums_users = db.relationship('User', secondary=user_albums, backref=db.backref('saved_users', lazy='dynamic'))

    # featured_artists = db.relationship('Artist', secondary=album_artists, backref=db.backref('albums_included', lazy='dynamic'))
    # genres = db.relationship('Genre', secondary=album_genres, backref=db.backref('albums_genres', lazy='dynamic'))

    def to_json(self):
        return {
            "album_id": self.id,
            "name": self.name,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "cover_art":self.cover_art,
            "albums_users": [{"album_id": user.id} for user in self.albums_users],
            "ranking": self.ranking if self.ranking else 0,  
            "descriptors": json.loads(self.descriptors) if self.descriptors else []  
        }
    
    def __repr__(self):
        return f" Album ID: {self.id}. Album name: {self.name}. Album Users: {[user.to_json() for user in self.albums_users]}"