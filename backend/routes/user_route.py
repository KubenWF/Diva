from flask import render_template,request,jsonify
from models import User

def register_users(app,db):

    @app.route("/users",methods=["GET"]) ## WORKS!!!!
    def get_users():
        users = User.query.all()
        json_users = list(map(lambda x: x.to_json(),users))
        return jsonify({"users":json_users}),200
        
    
    @app.route("/create_user",methods=["POST"]) ## WORKS!!!!
    def create_user():
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        birth_day = int(request.json.get('birth_day'))
        bio = request.json.get('bio')
        birth_year = int(request.json.get('birth_year'))
        birth_month = int(request.json.get('birth_day'))

        if not first_name or not last_name or not email or not birth_day or not birth_year or not birth_month:
            return jsonify({'message':'You missed one of the data points'}),400
                
        new_user = User(first_name=first_name,last_name=last_name,email=email,birth_day=birth_day,birth_month=birth_month,birth_year=birth_year,bio=bio)

        json_user = new_user.to_json()
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return (
            jsonify({'message':str(e)}),
            400
            )

        return jsonify({"message": "User added successfully","user": json_user}), 201

    @app.route('/delete_user/<id>', methods=['DELETE']) ## WORKS!!!!
    def delete_user(id):
        user = User.query.get(id)

        if not user:
            return jsonify({"message":"User not found"}),404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message":"User deleted"}),200

    @app.route('/details_user/<id>',methods=["GET"]) ## WORKS!!!!
    def details_user(id):
        user = User.query.filter(User.id==id).first()
        json_user = user.to_json()

        if not user:
            return jsonify({"message":"User not found"}),404

        return jsonify({"message": "User found","user": json_user}), 201

    @app.route('/update_user/<id>', methods=['PUT']) ## WORKS!!!!
    def update_user(id):
        user = User.query.get(id)

        if not user:
            return jsonify({"message":"User not found"}),404
        
        data = request.json
        user.first_name = data.get("first_name",user.first_name)
        user.last_name = data.get("last_name",user.last_name)
        user.email = data.get("email",user.email)
        user.bio = data.get("bio",user.bio)
        user.birth_day = data.get("birth_day",user.birth_day)
        user.birth_month = data.get("birth_month",user.birth_month)
        user.birth_year = data.get("birth_year",user.birth_year)

        db.session.commit()

        return jsonify({"message": "User updated"}), 201

    @app.route('/add_to_favorites/<user_id>/<album_id>', methods=['POST']) ## WORKS!!!!
    def add_album_favorites(user_id,album_id):
        from models import Album
    
        album = Album.query.get(album_id)
        if not album:
            return jsonify({'message': 'Album not found.'}), 404

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message":"User not found"}),404

        # Add album to user's favorite albums if not already added
        if album not in user.user_albums:
            user.user_albums.append(album)
            db.session.commit() 

            return jsonify({'message': 'Album added to your favorites!'}), 200
        else:
            return jsonify({'message': 'Album is already in your favorites.'}), 200

    @app.route("/albums_added/<int:user_id>", methods=["GET"])
    def get_added_albums(user_id):

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        albums = user.user_albums
        if not albums:
            return jsonify({"message": "No albums added by this user."}), 404

        json_albums = [album.to_json() for album in albums]

        return jsonify({"albums": json_albums}), 200