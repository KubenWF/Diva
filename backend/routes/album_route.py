from flask import render_template,request,jsonify
from models import Album
from datetime import datetime

def register_albums(app,db):
    
    @app.route("/albums",methods=["GET"]) ## WORKS!!!!
    def get_albums():
        albums = Album.query.all()
        json_albums = list(map(lambda x: x.to_json(),albums))
        return jsonify({"albums":json_albums}),200


    @app.route('/delete_album/<id>', methods=['DELETE']) ## WORKS!!!!
    def delete_album(id):
        album = Album.query.get(id)

        if not album:
            return jsonify({"message":"album not found"}),404
        
        db.session.delete(album)
        db.session.commit()
        
        return jsonify({"message":"album deleted"}),200

    @app.route('/details_album/<id>',methods=["GET"]) ## WORKS!!!!
    def details_album(id):
        album = Album.query.filter(Album.id==id).first()
        json_album = album.to_json()

        if not album:
            return jsonify({"message":"User not found"}),404

        return jsonify({"message": "User found","user": json_album}), 201

    
    @app.route('/update_album/<id>', methods=['PUT']) ## WORKS!!!!
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

    @app.route("/users_added/<int:album_id>", methods=["GET"]) ## WORKS!!!!
    def get_added_users(album_id):

        album = Album.query.get(album_id)
        if not album:
            return jsonify({"message": "Album not found"}), 404

        users = album.albums_users
        if not users:
            return jsonify({"message": "No users added by this user."}), 404

        json_users = [{"album_id": album.id} for album in users]

        return jsonify({"users": json_users}), 200