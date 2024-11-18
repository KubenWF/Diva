from flask import render_template,request,jsonify
from models import List,User

def register_lists(app,db):

    @app.route("/lists",methods=["GET"]) ## WORKS!!!!
    def get_lists():
        lists = List.query.all()
        json_lists = list(map(lambda x: x.to_json(),lists))
        return jsonify({"lists":json_lists}),200
        
    @app.route("/create_list/<int:user_id>", methods=["POST"])
    def create_list(user_id):
        # Retrieve the user object by user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

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