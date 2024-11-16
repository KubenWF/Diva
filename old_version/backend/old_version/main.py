from flask import request,jsonify
from config_initial import app,db
from models import User,Album,Artist,Genre,List,Review
from datetime import datetime

# Users
@app.route("/users",methods=["GET"])
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(),users))
    return jsonify({"users":json_users}),200

@app.route("/create_user",methods=["POST"])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    birth_date = request.json.get('birth_date')
    bio = request.json.get('bio')

    if not first_name or not last_name or not email or not birth_date or not bio:
        return jsonify({'message':'You missed one of the data points'}),400
            
    new_user = User(first_name=first_name,last_name=last_name,email=email,birth_date=birth_date,bio=bio)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return (
            jsonify({'message':str(e)}),
            400
            )

    return jsonify({"message":"user_created"}),201

@app.route("/update_user/<int:user_id>",methods=["PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message":"User not found"}),404
    
    data = request.json
    user.first_name = data.get("first_name",user.first_name)
    user.last_name = data.get("last_name",user.last_name)
    user.email = data.get("email",user.email)
    user.bio = data.get("bio",user.bio)
    user.birth_date = data.get("birth_date",user.birth_date)

    db.session.commit()

    return jsonify({"message":"User updated"}),200

@app.route("/delete_user/<int:user_id>",methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message":"User not found"}),404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message":"User deleted"}),200

# Lists
@app.route("/create_list/<int:user_id>", methods=["POST"])
def create_list(user_id):
    """Create a new list for a user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    list_name = request.json.get("list_name")
    if not list_name:
        return jsonify({"message": "List name is required"}), 400

    new_list = List(name=list_name, owner_id=user_id)

    try:
        db.session.add(new_list)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "List created", "list": new_list.to_json()}), 201

@app.route("/add_film_to_list/<int:list_id>", methods=["POST"])
def add_album_to_list(list_id):
    """Add a album to an existing list."""
    user_list = List.query.get(list_id)
    if not user_list:
        return jsonify({"message": "List not found"}), 404

    album_id = request.json.get("album_id")
    album = Album.query.get(album_id)  # Assuming `Album` represents a album

    if not album:
        return jsonify({"message": "album not found"}), 404

    user_list.albums.append(album)  # Assuming a many-to-many relationship

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "album added to list", "list": user_list.to_json()}), 200

@app.route("/remove_film_from_list/<int:list_id>/<int:album_id>", methods=["DELETE"])
def remove_album_from_list(list_id, album_id):
    """Remove a album from a list."""
    user_list = List.query.get(list_id)
    if not user_list:
        return jsonify({"message": "List not found"}), 404

    album = Album.query.get(album_id)
    if not album or album not in user_list.albums:
        return jsonify({"message": "album not found in the list"}), 404

    user_list.albums.remove(album)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "album removed from list", "list": user_list.to_json()}), 200


@app.route("/delete_list/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    """Delete a user's list."""
    user_list = List.query.get(list_id)
    if not user_list:
        return jsonify({"message": "List not found"}), 404

    try:
        db.session.delete(user_list)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "List deleted"}), 200


# Writing a Review or Rating an Album
@app.route("/albums/<int:album_id>/review", methods=["POST"])
def add_review(album_id):
    """Add a review and rating for an album."""
    user_id = request.json.get("user_id")
    rating = request.json.get("rating")
    review_text = request.json.get("review_text", "")

    # Validate the user and album
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    album = Album.query.get(album_id)
    if not album:
        return jsonify({"message": "Album not found"}), 404

    # Validate rating
    if rating is None or not (0 <= rating <= 5):
        return jsonify({"message": "Rating must be between 0 and 5"}), 400

    # Create the review
    review = Review(user_id=user_id, album_id=album_id, rating=rating, review_text=review_text, timestamp=datetime.now())

    try:
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Review added", "review": review.to_json()}), 201

# Getting Last 5 Activities of the User
@app.route("/users/<int:user_id>/recent_activities", methods=["GET"])
def get_recent_activities(user_id):
    """Retrieve the last 5 activities of a user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Fetch recent activities
    activities = []

    # Fetch user's reviews as activities
    reviews = Review.query.filter_by(user_id=user_id).order_by(Review.timestamp.desc()).limit(5).all()
    for review in reviews:
        activities.append({
            "type": "review",
            "album_id": review.album_id,
            "rating": review.rating,
            "review_text": review.review_text,
            "timestamp": review.timestamp.isoformat()
        })

    # Fetch other activities (e.g., favorite albums, lists created) - additional queries can be added
    favorite_albums = user.favorite_albums[-5:]
    for album in favorite_albums:
        activities.append({
            "type": "favorite_album",
            "album_id": album.album_id,
            "timestamp": album.timestamp.isoformat() if album.timestamp else None
        })

    owned_lists = user.owned_lists[-5:]
    for lst in owned_lists:
        activities.append({
            "type": "created_list",
            "list_id": lst.list_id,
            "name": lst.name,
            "timestamp": lst.created_at.isoformat() if lst.created_at else None
        })

    # Sort activities by timestamp and limit to last 5
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activities = activities[:5]

    return jsonify({"recent_activities": recent_activities}), 200



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

