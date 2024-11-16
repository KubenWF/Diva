from config_initial import db
from datetime import datetime,date


# Users-Albums( Users can add albums to their favourites)
favorite_albums = db.Table('favorite_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

# Users-Artists( Users can add artists to their favourites)
favorite_artists = db.Table('favorite_artists',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)

# Album-Artists
album_artists = db.Table('album_artists',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)

# Album-Genre
album_genres = db.Table('album_genres',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

#  List and Album
list_albums = db.Table('list_albums',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

# List and User for followers
list_followers = db.Table('list_followers',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(80),unique = False, nullable=False) # First name of the user
    last_name = db.Column(db.String(80),unique = False, nullable=False) # Last name of the user
    email = db.Column(db.String(120),unique = True, nullable=False) # Email of the user
    birth_date = db.Column(db.Date, nullable=False)  # Date of birth of the user
    bio = db.Column(db.Text, nullable=True)         # Bio of user

    favorite_artists = db.relationship('Artist', secondary=favorite_artists, backref=db.backref('artists_users', lazy='dynamic'))
    
    favorite_albums = db.relationship('Album', secondary=favorite_albums, backref=db.backref('albums_users', lazy='dynamic'))

    # Owned lists
    owned_lists = db.relationship('List', backref='owner', lazy=True)

    # Many-to-many relationship to lists (following lists)
    followed_lists = db.relationship('List', secondary=list_followers, backref=db.backref('lists_followed', lazy='dynamic'))

    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "bio": self.bio,
            "favorite_albums": [album.to_json() for album in self.favorite_albums],
            "favorite_artists": [artist.to_json() for artist in self.favorite_artists],
            "owned_lists": [lst.to_json() for lst in self.owned_lists],
            "followed_lists": [lst.to_json() for lst in self.followed_lists],
            "reviews": [review.to_json() for review in self.reviews]
        }

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Required rating out of 5
    review_text = db.Column(db.Text, nullable=True)  # Optional review text
    timestamp = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)

    # Foreign keys to link to User and Album
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)

    # Define relationships
    album = db.relationship('Album', backref=db.backref('reviews_album', lazy=True))

    def to_json(self):
        return {
            "review_id": self.id,
            "rating": self.rating,
            "review_text": self.review_text,
            "user_id": self.user_id,
            "album_id": self.album_id
        }
    
class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    release_date = db.Column(db.Date, nullable=True)  # Optional field for release date
    cover_art = db.Column(db.String(255), nullable=False)

    featured_artists = db.relationship('Artist', secondary=album_artists, backref=db.backref('albums_included', lazy='dynamic'))
    genres = db.relationship('Genre', secondary=album_genres, backref=db.backref('albums_genres', lazy='dynamic'))

    def to_json(self):
        return {
            "album_id": self.id,
            "name": self.name,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "cover_art":self.cover_art,
            "featured_artists": [artist.name for artist in self.featured_artists],
            "genres": [genre.name for genre in self.genres],
            "review": [review.to_json() for review in self.reviews]
        }

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    bio = db.Column(db.Text, nullable=True)         # Bio of the artist
    artist_photo = db.Column(db.String(255), nullable=True)
    
    # featured_albums = db.relationship('Album', secondary=album_artists, backref=db.backref('artists_included', lazy='dynamic'))

    def to_json(self):
        return {
            "artist_id": self.id,
            "name": self.name,
            "bio": self.bio,
            "artist_photo": self.artist_photo,
            "featured_albums": [album.name for album in self.albums_included]
        }

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    genre_photo = db.Column(db.String(255), nullable=True)

    def to_json(self):
        return {
            "genre_id": self.id,
            "name": self.name,
            "genre_photo": self.genre_photo
        }

class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=date.today, nullable=False)

    # ForeignKey for owner relationship (user who created the list)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Many-to-many relationship with albums (albums in the list)
    listed_albums = db.relationship('Album', secondary=list_albums, backref=db.backref('lists_associations', lazy='dynamic'))

    # Many-to-many relationship with followers of the list (followers in the list)
    followers = db.relationship('User', secondary=list_followers, backref=db.backref('lists_followed', lazy='dynamic'))

    def to_json(self):
        return {
            "list_id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner_id": self.owner_id,
            "listed_albums": [album.to_json() for album in self.listed_albums],
            "followers": [user.id for user in self.followers]
        }

