from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Correct case for SQLAlchemy configuration key
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"  # Fix the URI format here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


