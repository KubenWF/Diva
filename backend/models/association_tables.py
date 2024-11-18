from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey

# Users-Albums( Users can add albums to their favourites)
user_albums = db.Table('favorite_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True)
)

#  List and Album
list_albums = db.Table('list_albums',
    db.Column('list_id', db.Integer, db.ForeignKey('lists.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True)
)

owner_users_lists = db.Table(
    'owner_users_lists',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('list_id', db.Integer, db.ForeignKey('lists.id'), primary_key=True)
)
