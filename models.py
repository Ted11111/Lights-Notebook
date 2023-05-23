# models.py
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    author = db.Column(db.String(50)) # User that writes it down

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.username}>'
    
def create_db_tables():
    with current_app.app_context():
        db.create_all()