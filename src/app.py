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
from models import db, User, People, Favorite_people, Planet, Favorite_planet
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



@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# @app.route("/user/favorite", methods=["GET"])
# def get_user_favorite():
#     # pendientEE


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'birth_year': p.birth_year} for p in people])

@app.route("/people/<int:people_id>", methods=["GET"])
def get_character(people_id):
    character= People.query.get(people_id)
    if character: 
        character_detail= character.serialize()
        return jsonify(character_detail)
    else: 
        return jsonify({"msg":"character not found"}),404
    
@app.route("/favorite/people", methods= ["POST"])
def add_favorite_people():
    request_body= request.get_json()
    new_favoritepeople= Favorite_people(user_id=request_body["user_id"], people_id=request_body["people_id"])
    db.session.add(new_favoritepeople)
    db.session.commit()
    response= {"msg":"Favorito agregado"}
    return jsonify(response),200


@app.route("/planet", methods=["GET"])  
def get_all_planet():
    planet = Planet.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'population': p.population, "climate": p.climate} for p in planet])

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet= Planet.query.get(planet_id)
    if planet: 
        planet_detail= planet.serialize()
        return jsonify(planet_detail)
    else: 
        return jsonify({"msg":"planet not found"}),404
    
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet():
    request_body= request.get_json()
    new_favorite_planet= Favorite_planet(user_id=request_body["user_id"], people_id=request_body["planet_id"])
    db.session.add(new_favorite_planet)
    db.session.commit()
    response= {"msg":"Planeta favorito agregado"}
    return jsonify(response),200


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def del_favorite_person(people_id):
    request_body = request.get_json()  
    if not request_body or 'user_id' not in request_body:
        return jsonify({"msg": "Solicitud incorrecta, falta user_id"}), 400
    user_id = request_body['user_id']
    favorite_person = Favorite_people.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite_person is None:
        return jsonify({"msg": "Persona favorita no encontrada"}), 404
    db.session.delete(favorite_person)
    db.session.commit()
    
    response = {"msg": "Persona favorita eliminada"}
    return jsonify(response), 200

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def del_favorite_planet(planet_id):
    request_body = request.get_json()  
    if not request_body or 'user_id' not in request_body:
        return jsonify({"msg": "Solicitud incorrecta, falta user_id"}), 400
    user_id = request_body['user_id']
    favorite_planet= Favorite_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"msg": "planeta favorito no encontrado"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    
    response = {"msg": "Planeta favorito eliminado"}
    return jsonify(response), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
