from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey

# Users-Albums( Users can add albums to their favourites)
user_albums = db.Table('favorite_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)