from flask import render_template,request,jsonify,redirect,url_for
from models import User
from flask_login import login_user,logout_user,current_user,login_required

def register_users(app,db,bcrypt):

    @app.route("/users",methods=["GET"]) ## WORKS!!!!
    def get_users():
        users = User.query.all()
        json_users = list(map(lambda x: x.to_json(),users))
        return jsonify({"users":json_users}),200

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

    # @app.route('/add_to_favorites/<user_id>/<album_id>', methods=['POST']) ## WORKS!!!!
    # def add_album_favorites(user_id,album_id):
    #     from models import Album
    
    #     album = Album.query.get(album_id)
    #     if not album:
    #         return jsonify({'message': 'Album not found.'}), 404

    #     user = User.query.get(user_id)
    #     if not user:
    #         return jsonify({"message":"User not found"}),404

    #     # Add album to user's favorite albums if not already added
    #     if album not in user.user_albums:
    #         user.user_albums.append(album)
    #         db.session.commit() 

    #         return jsonify({'message': 'Album added to your favorites!'}), 200
    #     else:
    #         return jsonify({'message': 'Album is already in your favorites.'}), 200

    @app.route("/albums_added/<int:user_id>", methods=["GET"]) ## WORKS!!!!
    def get_added_albums(user_id):

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        albums = user.user_albums
        if not albums:
            return jsonify({"message": "No albums added by this user."}), 404

        json_albums = [{"album_id": album.id,"album_name": album.name,"album_cover_art": album.cover_art,"album_ranking": album.ranking} for album in albums]

        return jsonify({"albums": json_albums}), 200

    @app.route("/index",methods=["GET","POST"])
    def index():
        if current_user.is_authenticated:
            return jsonify({"User ID":str(current_user.id),'message': 'User logged in!'}), 200
        else:
            return "No user is logged in"    

    @app.route("/signup",methods=["GET","POST"])
    def signup():
        if request.method == "GET":
            return jsonify({'message': 'Sign up success!'}), 200
        elif request.method == "POST":
            user_name = request.json.get('user_name')
            password = str(request.json.get('password'))
            email = request.json.get('email')
            birth_day = int(request.json.get('birth_day'))
            birth_month = int(request.json.get('birth_month'))
            birth_year = int(request.json.get('birth_year'))
            bio = request.json.get('bio')

            hashed_password = bcrypt.generate_password_hash(password)

            hashed_password = hashed_password.decode("utf-8")

            user = User(user_name = user_name,password = hashed_password,email=email,birth_day = birth_day,birth_month = birth_month,birth_year=birth_year,bio=bio)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))


    @app.route("/login",methods=["GET","POST"])
    def login():
        if request.method == "GET":
            return jsonify({'message': 'Login success!'}), 200
        elif request.method == "POST":
            user_name = request.json.get('user_name')
            password = request.json.get('password')

            user = User.query.filter(User.user_name == user_name).first()

            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return (f"Logged in user: {current_user}")
                # return jsonify({"User name":str(user.user_name),'message': 'User logged in!'})
            else:
                return "Failed"

    @app.route("/update_user", methods=["PUT"])
    @login_required
    def update_user():
        user = current_user  # Access the logged-in user

        # Extract fields to be updated from the request body
        updated_user_name = request.json.get('user_name', user.user_name)
        updated_email = request.json.get('email', user.email)
        updated_password = request.json.get('password', user.password)
        updated_bio = request.json.get('bio', user.bio)
        updated_birth_day = request.json.get('birth_day', user.birth_day)
        updated_birth_month = request.json.get('birth_month', user.birth_month)
        updated_birth_year = request.json.get('birth_year', user.birth_year)

        hashed_password = bcrypt.generate_password_hash(updated_password)

        hashed_password = hashed_password.decode("utf-8")

        # Update user fields
        user.user_name = updated_user_name
        user.email = updated_email
        user.bio = updated_bio
        user.birth_day = updated_birth_day
        user.birth_month = updated_birth_month
        user.birth_year = updated_birth_year
        user.password = hashed_password

        # Save changes to the database
        db.session.commit()

        return jsonify({'message': 'User information updated successfully!', 'user': user.to_json()}), 200

    @app.route("/delete", methods=["DELETE"])
    @login_required
    def delete_account():
        user = current_user
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User account deleted successfully!'}), 200

    @app.route("/add_album_favourites", methods=['POST'])
    @login_required
    def add_album_favourites():
        from models import Album
        album_id = request.json.get('album_id')
        album = Album.query.get(int(album_id))
        if not album:
            return jsonify({'message': 'Album not found.'}), 404

        user = current_user

        # Add album to user's favorite albums if not already added
        if album not in user.user_albums:
            user.user_albums.append(album)
            db.session.commit() 

            return jsonify({'message': 'Album added to your favorites!'}), 200
        else:
            return jsonify({'message': 'Album is already in your favorites.'}), 200

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return "Success"