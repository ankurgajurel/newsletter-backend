from flask import Flask, jsonify, request, redirect
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


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

## Add a new subscriber to the database
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
    
# Retrieve a subscriber from the database using their email    
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
    
# Delete a subscriber from the database using their email
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
    
# Update a subscriber's email or full name   
@app.route('/updateSubscriber', methods=['PUT'])
def update_subscriber():
    data = request.get_json()
    email = data.get('email')
    newEmail = data.get('newEmail')
    newFullName = data.get('newFullName')

    if email:
        existing_user = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing_user:
            if newEmail:
                existing_user.email = newEmail
            if newFullName:
                existing_user.fullName = newFullName
            db.session.commit()
            return jsonify(message='Subscriber has been updated'), 200
        else:
            return jsonify(message='Subscriber does not exist'), 400
    else:
        return jsonify(message='Missing email'), 400
    
# Retrieve all subscribers from the database
@app.route('/getAllSubscribers', methods=['GET'])
def get_all_subscribers():
    subscribers = NewsletterSubscriber.query.all()
    all_subscribers = []
    for subscriber in subscribers:
        subscriber_data = {}
        subscriber_data['fullName'] = subscriber.fullName
        subscriber_data['email'] = subscriber.email
        all_subscribers.append(subscriber_data)
    return jsonify(all_subscribers), 200

# docs for the apu
@app.route('/docs', methods=['GET'])
def docs():
    return redirect('/static/swagger.json')

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Newsletter Subscription API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

####################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="4040")