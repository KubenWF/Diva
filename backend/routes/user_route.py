from flask import Blueprint,render_template,request,jsonify,redirect,url_for
from models import User
from flask_login import login_user,logout_user,current_user,login_required

def register_user(app,db,bcrypt):
    """Routes for authenticated users to manage their own resources (e.g., create/edit/delete personal lists, follow lists)."""
    user_bp = Blueprint('user', __name__)
 
    @user_bp.route("/index",methods=["GET","POST"]) ## WORKS!!!!
    def index():
        if current_user.is_authenticated:
            return jsonify({"User ID":str(current_user.id),'message': 'User logged in!'}), 200
        else:
            return "No user is logged in"    

    @user_bp.route("/update_user", methods=["PUT"]) ## WORKS!!!!
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

    @user_bp.route("/delete_account", methods=["DELETE"]) ## WORKS!!!!
    @login_required
    def delete_account():
        user = current_user
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User account deleted successfully!'}), 200

    @user_bp.route("/like_album", methods=['POST']) ## WORKS!!!!
    @login_required
    def like_album():
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

            return jsonify({'message': 'Album added to your liked albums!'}), 200
        else:
            return jsonify({'message': 'Album is already in your liked albums.'}), 200

    @user_bp.route("/create_list", methods=["POST"])
    @login_required
    def create_list():
        from models import List
        user = current_user

        list_name = request.json.get("list_name")
        list_description = request.json.get("list_description")
        if not list_name:
            return jsonify({"message": "List name is required"}), 400
        
        # Create the new list, passing the User object to the owners relationship
        new_list = List(name=list_name, description=list_description)

        try:
            # Add the user to the list's owners relationship
            new_list.owners.append(user)
            
            # Add the new list to the session
            db.session.add(new_list)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 400

        return jsonify({
            "message": "List created successfully",
            "list": new_list.to_json()
        }), 201

    @user_bp.route("/delete_list", methods=["DELETE"]) ## WORKS!!!!
    @login_required
    def delete_list():
        from models import List
        list_id = request.json.get("list_id")
        list = List.query.get(list_id)

        if current_user not in list.owners:
            return jsonify({'message': 'You do not have permission to delete this list'}), 403

        db.session.delete(list)
        db.session.commit()

        return jsonify({'message': 'List deleted successfully!'}), 200

    @user_bp.route("/add_album_list", methods=["POST"])
    @login_required
    def add_album_list():
        from models import List, Album
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON data"}), 400

        album_id = data.get('album_id')
        list_id = data.get("list_id")

        if not album_id:
            return jsonify({"message": "Album ID is required"}), 400
        if not list_id:
            return jsonify({"message": "List ID is required"}), 400

        try:
            album_id = int(album_id)  # Ensure that album_id is an integer
            list_id = int(list_id)    # Ensure that list_id is an integer
        except ValueError:
            return jsonify({"message": "Invalid ID format. Album ID and List ID should be integers."}), 400 

        album = Album.query.get(album_id)
        if not album:
            return jsonify({"message": "Album not found"}), 404

        user_list = List.query.filter(List.id == list_id, List.owners.any(id=current_user.id)).first()
        if not user_list:
            return jsonify({"message": "List not found or not owned by the user"}), 404

        try:
            if album in user_list.listed_albums:
                return jsonify({"message": "Album already exists in the list"}), 400

            user_list.listed_albums.append(album)
            db.session.commit()

            return jsonify({
                "message": "Album added to the list successfully",
                "list": user_list.to_json()
            }), 200
        except Exception as e:
            db.session.rollback()  # Ensure the session state is clean in case of an error
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    @user_bp.route("/delete_album_list", methods=["DELETE"])
    @login_required
    def delete_album_list():
        from models import List, Album
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON data"}), 400

        album_id = data.get('album_id')
        list_id = data.get("list_id")

        if not album_id or not list_id:
            return jsonify({"message": "Album ID and List ID are required"}), 400

        try:
            album_id = int(album_id)
            list_id = int(list_id)
        except ValueError:
            return jsonify({"message": "Invalid ID format. Please provide valid integers for album_id and list_id."}), 400

        album = Album.query.get(album_id)
        if not album:
            return jsonify({"message": "Album not found"}), 404

        user_list = List.query.filter(List.id == list_id, List.owners.any(id=current_user.id)).first()
        if not user_list:
            return jsonify({"message": "List not found or not owned by the user"}), 404

        try:
            if album not in user_list.listed_albums:
                return jsonify({"message": "Album not exists in the list"}), 400

            user_list.listed_albums.remove(album)
            db.session.commit()

            return jsonify({
                "message": "Album deleted from the list successfully",
                "list": user_list.to_json()
            }), 200
        except Exception as e:
            db.session.rollback()  # Ensure the session state is clean in case of an error
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    @user_bp.route("/logout") ## WORKS!!!!
    @login_required
    def logout():
        try:
            logout_user()
            return jsonify({"message": "Logged out successfully."}), 200
        except Exception as e:
            return jsonify({"message": "Failed to log out.", "error": str(e)}), 500

    app.register_blueprint(user_bp, url_prefix='/user')