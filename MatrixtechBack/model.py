from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)
    city = db.Column(db.String(255),  nullable = False)
    country = db.Column(db.String(255),  nullable = False)
