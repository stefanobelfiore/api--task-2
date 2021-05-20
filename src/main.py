"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Tasks
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all():
        all_users = User.get_all()

        return jsonify(all_users), 200

@app.route('/user/<email>', methods=['GET'])
def get_users_by_email(email):
    user = User.get_by_email(email)

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(user), 200

@app.route('/tasks/<user_id>', methods=['GET'])
def get_tasks_by_user(user_id):
    task = Tasks.get_tasks_by_user(user_id)

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(task), 200

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
        tasks = Tasks.get_all_tasks()

        return jsonify(tasks), 200


@app.route('/user', methods=['POST'])
def create_user():
    email, password = request.json.get("email", None),request.json.get("password", None)
    new_user = User(email=email, _password=password)
    return jsonify(new_user.create()), 201

@app.route('/tasks', methods=['POST'])
def create_task():
    description = request.json.get("description", None)
    new_description = Tasks(description=description)
    return jsonify(new_description.create()), 201    
    
@app.route('/user/<email>', methods=['DELETE'])
def delete_user(email):
    print(email,"papapapapapapapapapapapapapappapap")
    user = User.get_by_email(email)
    print(user,"pepepepepepepepepepepepepepepeep")
    if user:
        user_del = user.delete()
        return jsonify(user_del), 204
    else:
        return 'That username does not exist', 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)