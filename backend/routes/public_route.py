from flask import Blueprint,render_template,request,jsonify,redirect,url_for
from models import User
from flask_login import login_user,logout_user,current_user,login_required

def register_public(app,db,bcrypt):
    public_bp = Blueprint('public', __name__)

    @public_bp.route("/signup",methods=["GET","POST"]) ## WORKS!!!!
    def signup():
        if request.method == "GET":
            return jsonify({'message': 'Change it to POST method, dumby!'}), 200
        elif request.method == "POST":
            user_name = request.json.get('user_name')
            password = str(request.json.get('password'))
            email = request.json.get('email')
            birth_day = int(request.json.get('birth_day'))
            birth_month = int(request.json.get('birth_month'))
            birth_year = int(request.json.get('birth_year'))
            bio = request.json.get('bio')

            # Validate inputs
            if not user_name or not password or not email or not birth_day or not birth_month or not birth_year or not bio:
                return jsonify({"message": "Username, password, and email are required."}), 400

            if User.query.filter_by(user_name=user_name).first():
                return jsonify({"message": "Username is already taken."}), 409

            hashed_password = bcrypt.generate_password_hash(password)

            hashed_password = hashed_password.decode("utf-8")
            try:
                user = User(user_name = user_name,password = hashed_password,email=email,birth_day = birth_day,birth_month = birth_month,birth_year=birth_year,bio=bio)
                db.session.add(user)
                db.session.commit()
                return jsonify({"message": "Signup successful. Please log in."}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Error occurred during signup.", "error": str(e)}), 500

    @public_bp.route("/login",methods=["GET","POST"]) ## WORKS!!!!
    def login():
        if request.method == "GET":
            return jsonify({'message': 'Change to POST dumby!'}), 200
        elif request.method == "POST":
            user_name = request.json.get('user_name')
            password = request.json.get('password')

            if not user_name or not password:
                return jsonify({"message": "Username and password are required."}), 400

            user = User.query.filter(User.user_name == user_name).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                return jsonify({"message": "Invalid username or password."}), 401

            try:
                login_user(user)
                return jsonify({"message": f"Logged in as {current_user.user_name}"}), 200
            except Exception as e:
                return jsonify({"message": "Failed to log in.", "error": str(e)}), 500

    app.register_blueprint(public_bp,url_prefix='/public')
