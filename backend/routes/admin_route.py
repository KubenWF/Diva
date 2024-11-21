from flask import Blueprint,render_template,request,jsonify,redirect,url_for
from models import User,List,Album

def register_admin(app,db):
    """ Routes for for administrative actions (e.g., managing users, approving content, or viewing system logs)"""
    admin_bp = Blueprint('admin', __name__)

    @admin_bp.route('/delete_user/<id>', methods=['DELETE']) ## WORKS!!!!
    def delete_user(id):
        user = User.query.get(id)

        if not user:
            return jsonify({"message":"User not found"}),404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message":"User deleted"}),200

    @admin_bp.route('/user/<id>',methods=["GET"]) ## WORKS!!!!
    def details_user(id):
        user = User.query.filter(User.id==id).first()
        json_user = user.to_json()

        if not user:
            return jsonify({"message":"User not found"}),404

        return jsonify({"message": "User found","user": json_user}), 201

    @admin_bp.route("/albums_added/<int:user_id>", methods=["GET"]) ## WORKS!!!!
    def get_added_albums(user_id):

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        albums = user.user_albums
        if not albums:
            return jsonify({"message": "No albums added by this user."}), 404

        json_albums = [{"album_id": album.id,"album_name": album.name,"album_cover_art": album.cover_art,"album_ranking": album.ranking} for album in albums]

        return jsonify({"albums": json_albums}), 200
    
    @admin_bp.route('/list/<id>',methods=["GET"]) ## WORKS!!!!
    def details_list(id):
        list = List.query.filter(List.id==id).first()
        json_list = list.to_json()

        if not list:
            return jsonify({"message":"List not found"}),404

        return jsonify({"message": "List found","List": json_list}), 201

    @admin_bp.route('/delete_list/<id>', methods=['DELETE']) ## WORKS!!!!
    def delete_list(id):
        list = List.query.get(id)

        if not list:
            return jsonify({"message":"list not found"}),404
        
        db.session.delete(list)
        db.session.commit()
        
        return jsonify({"message":"list deleted"}),200

    @admin_bp.route('/delete_album/<id>', methods=['DELETE']) ## WORKS!!!!
    def delete_album(id):
        album = Album.query.get(id)

        if not album:
            return jsonify({"message":"album not found"}),404
        
        db.session.delete(album)
        db.session.commit()
        
        return jsonify({"message":"album deleted"}),200

    @admin_bp.route('/album/<id>',methods=["GET"]) ## WORKS!!!!
    def details_album(id):
        album = Album.query.filter(Album.id==id).first()
        json_album = album.to_json()

        if not album:
            return jsonify({"message":"Album not found"}),404

        return jsonify({"message": "Album found","Album": json_album}), 201

    @admin_bp.route('/update_album/<id>', methods=['PUT']) ## WORKS!!!!
    def update_album(id):
        album = Album.query.get(id)

        if not album:
            return jsonify({"message":"album not found"}),404
        
        data = request.json
        album.name = data.get("name",album.name)
        album.release_date = datetime.strptime(data.get("release_date",album.release_date),'%Y-%m-%d').date()
        album.cover_art = data.get("cover_art",album.cover_art)
        album.ranking = data.get("ranking",album.ranking)
        album.descriptors = str(data.get("descriptors",album.descriptors))


        db.session.commit()

        return jsonify({"message": "album updated"}), 201
    
    @admin_bp.route("/users_added/<int:album_id>", methods=["GET"]) ## WORKS!!!!
    def get_added_users(album_id):

        album = Album.query.get(album_id)
        if not album:
            return jsonify({"message": "Album not found"}), 404

        users = album.albums_users
        if not users:
            return jsonify({"message": "No users added by this user."}), 404

        json_users = [{"album_id": album.id} for album in users]

        return jsonify({"users": json_users}), 200
    
    app.register_blueprint(admin_bp, url_prefix='/admin')