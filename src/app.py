"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

# -------------------------------User------------------------------

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/user/<string:item_id>', methods=['GET'])
def get_user(item_id):

    user = User.query.get(item_id)
    if user is None:
        abort(404)
    return jsonify(user.serialize()), 200

# -------------------------------People------------------------------

@app.route('/people', methods=['GET'])
def get_people():

    people= People.query.all()

    if people is None:
        abort(404)


    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<string:person_id>', methods=['GET'])
def get_person(person_id):

    person = People.query.get(person_id)

    if person is None:
        abort(404)

    return jsonify(person.serialize())

@app.route('/people', methods=['POST'])
def post_people():
    newPerson = People(name=request.json['name'])

    db.session.add(newPerson)
    db.session.commit()

    if newPerson is None:
        abort(404)

    return jsonify(newPerson.serialize())

@app.route('/people/<string:people_id>', methods=['PUT'])
def update_people(people_id):
    people = People.query.get(people_id)

    people.name = request.json['name']

    if people is None:
        abort(404)

    db.session.commit()
    return (jsonify(people.serialize()))

# -------------------------------Planets------------------------------

@app.route('/planets', methods=['GET'])
def get_planets():

    all_planets = {
        'msg':'all Planets'
    }

    return jsonify(all_planets), 200


# -------------------------------Favorites------------------------------

@app.route('/favorites', methods=['GET'])
def get_favorites():

    all_favorites = {
        'msg':'all favorites'
    }

    return jsonify(all_favorites), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
