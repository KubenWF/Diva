from app import db
from flask_login import UserMixin
from .association_tables import list_albums, list_owners,list_followers
from datetime import datetime,date

class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False,index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=date.today, nullable=False)

    owners = db.relationship('User',secondary= list_owners,backref=db.backref('listsowners', lazy='dynamic'))

    listed_albums = db.relationship('Album', secondary=list_albums, backref=db.backref('lists_associations', lazy='dynamic'))

    followers = db.relationship('User', secondary=list_followers, backref=db.backref('lists_followed', lazy='dynamic'))

    def to_json(self):
        return {
            "list_id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "listed_albums": [listed_album.id for listed_album in self.listed_albums]
        }