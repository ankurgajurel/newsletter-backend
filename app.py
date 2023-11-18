from flask import Flask, jsonify, request, redirect
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(500))
    email = db.Column(db.String(80), unique=True)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def index():
    return jsonify(message='This is the newsletter API')

@app.route('/newSubscriber', methods=['POST'])
def add_new_subscriber():
    data = request.get_json()
    fullName = data.get('fullName')
    email = data.get('email')

    if fullName and email:
        existing_user = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing_user:
            return jsonify(message='A user with this email already exists'), 409
        else:
            new_user = NewsletterSubscriber(fullName=fullName, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message='New Subscriber has been added to the database'), 201
    else:
        return jsonify(message='Missing fullName or email'), 400
    
@app.route('/getFullName', methods=['POST'])
def get_full_name():
    data = request.get_json()
    email = data.get('email')

    if email:
        existing_user = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing_user:
            fullName = existing_user.fullName
            return jsonify(message="The full name of the user with the email you provided is: " + fullName), 200
        else:
            return jsonify(message='The user has either been deleted or does not exist'), 400
    else:
        return jsonify(message='Missing email'), 400

@app.route('/deleteSubscriber', methods=['DELETE'])
def delete_subscriber():
    data = request.get_json()
    email = data.get('email')

    if email:
        existing_user = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            return jsonify(message='Subscriber has been deleted'), 200
        else:
            return jsonify(message='Subscriber does not exist'), 400
    else:
        return jsonify(message='Missing email'), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="4040")