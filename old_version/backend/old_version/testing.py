from datetime import date
from config_initial import app,db
from models import User, Album, Artist, Genre, List

def add_sample_data():
    # Add sample users
    user1 = User(first_name="John", last_name="Doe", email="john@example.com", birth_date=date(1990, 5, 17), bio="Music lover")
    user2 = User(first_name="Jane", last_name="Smith", email="jane@example.com", birth_date=date(1985, 8, 24), bio="Fan of rock music")
    
    # Add sample albums
    album1 = Album(name="Revolver", release_date=date(1966, 8, 5), cover_art="revolver_cover.jpg")
    album2 = Album(name="The Dark Side of the Moon", release_date=date(1973, 3, 1), cover_art="dark_side_cover.jpg")
    
    # Add sample artists
    artist1 = Artist(name="The Beatles", bio="A famous rock band", artist_photo="beatles_photo.jpg")
    artist2 = Artist(name="Pink Floyd", bio="Iconic progressive rock band", artist_photo="pink_floyd_photo.jpg")
    
    # Add sample genres
    genre1 = Genre(name="Rock", genre_photo="rock_photo.jpg")
    genre2 = Genre(name="Psychedelic Rock", genre_photo="psychedelic_rock_photo.jpg")
    
    # Add a sample list for a user
    list1 = List(name="My Favorite Albums", description="A list of my favorite albums", owner_id=1, created_at=date.today())

    # Add these records to the session
    db.session.add_all([user1, user2, album1, album2, artist1, artist2, genre1, genre2, list1])
    
    try:
        db.session.commit()
        print("Sample data added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding sample data: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_sample_data()  # Call the function to add sample data
    app.run(debug=True)
