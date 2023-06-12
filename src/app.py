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
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/user/<string:item_id>', methods=['GET'])
def get_user(item_id):

    user = User.query.get(item_id)
    if user is None:
        abort(404)
    return jsonify(user.serialize()), 200


@app.route('/user/<string:user_id>/favorites')
def get_userfav(user_id):

    user = User.query.get(user_id)
    planet = Planets.query.get(user_id)

    if user is None:
        abort(404)
    return jsonify(user.serialize(), planet.serialize()), 200

# -------------------------------People------------------------------


@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()

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


@app.route('/people/<string:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.get(people_id)

    db.session.delete(person)
    db.session.commit()
    return jsonify({'result': 'success'})

# -------------------------------Planets------------------------------


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()

    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<string:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planets.query.get(planet_id)

    if planet is None:
        abort(404)

    return jsonify(planet.serialize())


@app.route('/planets', methods=['POST'])
def post_planets():
    newplanet = Planets(name=request.json['name'])

    db.session.add(newplanet)
    db.session.commit()

    if newplanet is None:
        abort(404)

    return jsonify(newplanet.serialize())


@app.route('/planets/<string:planets_id>', methods=['PUT'])
def update_planets(planets_id):

    planets = Planets.query.get(planets_id)

    planets.name = request.json['name']

    if planets is None:
        abort(404)

    db.session.commit()
    return (jsonify(planets.serialize()))


@app.route('/planets/<string:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    db.session.delete(planet)
    db.session.commit()
    return jsonify({'result': 'success'})
# -------------------------------Favorites------------------------------


@app.route('/favorites', methods=['GET'])
def Favorites_todos():

    query = Favorites.query.all()
    results = list(map(lambda x: x.serialize2(), query))

    return jsonify(results), 200


@app.route('/favorites/<int:id>', methods=['GET'])
def favoritos_unico(id):

    favoritos = Favorites.query.get(id)
    if favoritos is None:
        raise APIException('Favorito not found', status_code=404)
    results = favoritos.serialize2()

    return jsonify(results), 200


@app.route('/favorites', methods=['POST'])
def add_Favorites():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    fav = Favorites(usuario_id=request.json['user_id'],
                    planeta_id=request.json["planets_id"],
                    personaje_id=request.json["people_id"])

    db.session.add(fav)
    db.session.commit()

    return jsonify("Un exito, se ha agregado el favorito"), 200


@app.route('/del_favorites/<int:id>', methods=['DELETE'])
def del_fav(id):

    # recibir info del request

    fav = Favorites.query.get(id)
    if fav is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(fav)

    db.session.commit()

    return jsonify("Borraste bien la informacion"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
