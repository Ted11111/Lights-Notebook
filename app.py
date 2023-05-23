# app.py
import os
import sqlite3
import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Person, create_db_tables, User

app = Flask(__name__)

# Database Connection
basedir = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists(os.path.join(basedir, 'notebook.sqlite')):
    conn = sqlite3.connect(os.path.join(basedir, 'notebook.sqlite'))
    conn.close()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notebook.sqlite')

db.init_app(app)

with app.app_context():
    create_db_tables()

engine = create_engine('sqlite:///' + os.path.join(basedir, 'notebook.sqlite'))
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/<string:username>/<string:password>', methods=['GET', 'POST']) #Login Page
def home(username, password):
    if request.method == 'GET': #This will compare pass and user with user stored in db
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                return("Logged in!")
            else:
                return("Login Failed")
        else:
            return "Login Failed"
    elif request.method == 'POST':
        hashpassword = password.encode('utf-8')  # Convert the password to bytes
        salt = bcrypt.gensalt()  # Generate a salt
        hashed_password = bcrypt.hashpw(hashpassword, salt)

        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        
        return "User registered & Logged In"

@app.route('/entries', methods=['GET']) #Notebook Page (Protected Page)
def entries():
    # Retrieve all people from the Person model
    people = session.query(Person).all()
    
    # Select desired attributes and create a list of dictionaries
    result = [
        {'first_name': person.first_name, 'last_name': person.last_name}
        for person in people
    ]
    
    return jsonify(result)

@app.route('/entries/<string:first_name>/<string:last_name>', methods=['GET', 'POST', 'DELETE'])
def entry(first_name, last_name):
    if request.method == 'GET':
        # Retrieve people by first name and last name
        people = session.query(Person).filter_by(first_name=first_name, last_name=last_name).all()
        
        # Select desired attributes and create a list of dictionaries
        result = [
            {'first_name': person.first_name, 'last_name': person.last_name}
            for person in people
        ]
        
        return jsonify(result)
    
    elif request.method == 'POST':
        # Add a new person to the Person model
        new_person = Person(first_name=first_name, last_name=last_name)
        session.add(new_person)
        session.commit()
        
        return "Person added successfully"
    elif request.method == 'DELETE':
        # Find the person by first name and last name
        person = session.query(Person).filter_by(first_name=first_name, last_name=last_name).first()
    
        if person:
            # Delete the person from the database
            session.delete(person)
            session.commit()
        
            return "Person deleted successfully"
        else:
            return "Person not found"

if __name__ == '__main__':
    app.run()