import os
import csv
from models import Album
import pandas as pd

def import_csv_to_db(app,db):
    with app.app_context():
        album_file_path = os.path.join('instance', 'albums.csv')

        df = pd.read_csv(album_file_path, delimiter='\t')

        for index, row in df.iterrows():
            album = Album(
                id=int(index),
                name=row['name'],
                billboard=row['billboard'] if row['billboard'] else None,
                artists=row['artists'] if row['artists'] else None,
                total_tracks=int(row['total_tracks']) if row['total_tracks'] else None,
                album_type=row['album_type'] if row['album_type'] else None,
                image_url=row['image_url'] if row['image_url'] else None
            )
            db.session.add(album)

        db.session.commit()





