from app import create_app
from import_data import import_csv_to_db
from flask import current_app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0',debug=True)

