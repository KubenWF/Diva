from flask import render_template,request
from models import User

def register_users(app,db):
    
    @app.route('/',methods = ['GET','POST'])
    def index():
        if request.method == 'GET':
            users = User.query.all()
            return render_template('index.html',users = users)
        elif request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            bio = request.form.get('bio')
            birth_day = int(request.form.get('birth_day'))
            birth_month = int(request.form.get('birth_month'))
            birth_year = int(request.form.get('birth_year'))
            
            # Check if the email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                error_message = "The email address is already in use. Please use a different one."
                users = User.query.all()
                return render_template('index.html', users=users, error_message=error_message)

            
            user = User(first_name=first_name,
                        last_name = last_name,
                        email=email,
                        bio=bio,
                        birth_day=birth_day,
                        birth_month=birth_month,
                        birth_year=birth_year
                        )
            
            db.session.add(user)
            db.session.commit()

            users = User.query.all()
            return render_template('index.html',users = users)




    # @app.route('/delete_user/<int:id>', methods=['DELETE'])
    # def delete_user(id):
    #     User.query.filter(User.id==id).delete()

    #     db.session.commit()
        
    #     users = User.query.all()
    #     return render_template('index.html',users = users)