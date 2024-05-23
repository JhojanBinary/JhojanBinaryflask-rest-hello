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
from models import db, User, Planets, Person, FavoritePlanets,Addres
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




#METODO PARA CONSULTAR A TODOS LOS USUARIOS
@app.route('/people', methods=['GET'])
def handle_hello():
    #sqlalchemy sintax
    all_users = User.query.all()
    user_serialized = []
    for user in all_users:
        user_serialized.append(user.serialize())
    print(user_serialized)
    return jsonify({"data" : user_serialized}), 200




#METODO PARA CONSULTAR A USUARIOS POR SU ID
@app.route("/people/<int:id>", methods=[ 'GET' ])
def get_people_user (id):

    single_people = User.query.get (id)
    if single_people is None:
         return jsonify({"msg": "El usuario con el ID: {} no existe".format(id)}), 400

         #retorna al usuario seleccionado por su id mostrando todos   
         #sus datos
    return jsonify({"data": single_people.serialize()}), 200





#[GET] /planets Listar todos los registros de planets en la base de datos.
@app.route('/planets',methods = ['GET'])
def get_planets():
    all_planets = Planets.query.all()

    planet_serialized = []

    for planet in all_planets:
        planet_serialized.append(planet.serialize())
    print(planet_serialized)

    return jsonify({"planetas" : planet_serialized}),200





#[GET] /planets/<int:planet_id> Muestra la información de un solo planeta según su id.

@app.route('/planets/<int:planet_id>', methods =['GET'])
def get_single_planet(planet_id):

    single_planet = Planets.query.get(planet_id)
    if single_planet is None:
        return jsonify({'msg' : 'El planeta con el ID: {} no existe'.format(planet_id)}),400
    
    return jsonify({'data' : single_planet.serialize()}),200





#[GET] /users Listar todos los usuarios del blog.
@app.route('/users', methods = ['GET'])
def get_users():
    all_users = Person.query.all()
    user_serialized = []

    for user in all_users:
        user_serialized.append(user.serialize())
    print(user_serialized)
    return jsonify({"data" : user_serialized}),200


#[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.

# @app.route('/favorites', methods = ['GET'])
# def get_favorites_planets():
#     all_favories = FavoritePlanets.query.all()
#     favorites_serialized = []

#     for favorites in all_favories:
#         favorites_serialized.append(favorites.serialize())

#     print(favorites_serialized)
#     return jsonify({"data" : favorites_serialized}),200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    usuario = User.query.get(user_id)
    
    if usuario is None:
        return jsonify({"msg": f"Usuario con ID {user_id} no existe"}), 404
                                                  #LA COLUMNA QUE QUIERO LLAMAR
                                                #USUARIO CON PLANEETAS FAVORITOS #3 
    '''favorite_planets = FavoritePlanets.query.filter_by(user_id = id).all() #.all me duevuele a todos los usuarios que tienene un planeta favorito'''
    '''
     forma 1
    favorite_planets_serialized = []
        #creo una variable para contar los datos de - favorite_planets
        #para luego meterlos en - favorite_planets_serialized
    for favorite_planet in favorite_planets: 
        favorite_planets_serialized.append(favorite_planet.seralize())

    #Forma 2 - mas corta
    favorite_planets_serialized = list(map(lambda planeta : planeta.serialized(), favorite_planets))
    '''

    favorite_planets = db.session.query(FavoritePlanets, Planets).join(Planets)\
                      .filter(FavoritePlanets.user_id == user_id).all()

    favorite_planets_serialized = []
    for favorite_planet, planet in favorite_planets:
        favorite_planets_serialized.append({
            'favorite_planet_id': favorite_planet.id, 
            'planet': planet.serialize(),
            'user_id': user_id
        })

    return jsonify({"msg": "ok", "favorite_planets": favorite_planets_serialized}), 200





@app.route("/planet", methods=['POST'])
def new_planet():
    body = request.get_json(silent = True)
    if body is None:
        return jsonify({"msg" : "Debes enviar info en el body"}),400
    
    if "name" not in body:
        return jsonify({"msg" :"name es requerido"}),400

    if "population" not in body:
        return jsonify({"msg" :"population es requerido"}),400


    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body ["population"]
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg" : "Nuevo planeta creado",
                    "data" : new_planet.serialize()}),201


# [POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
@app.route('/people', methods = ['POST'])

def add_people():
    body = request.get_json(silent = True)

    if body is None:
        return jsonify({"alerta" : "EL CONTENIDO ESTÁ VACIO"}),400

    if "account" not in body:
        return jsonify({"alerta" : "EL CAMPO account ES REQUERIDO"}),400

    if "apell" not in body:
        return jsonify({"alerta" : "EL CAMPO apell ES REQUERIDO"}),400

    if "name" not in body:
        return jsonify({"alerta" : "EL CAMPO name ES REQUERIDO"}),400
    
    new_people = Person()
    new_people.account = body ["account"]
    new_people.apell = body ["apell"]
    new_people.name = body ["name"]

    db.session.add(new_people)
    db.session.commit()

    return jsonify({"msg" : "PLANETA CREADO",
                    "valor creado" : new_people.serialize()}),201


# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.

@app.route("/favorite/planet/<int:planet_id>",methods=["DELETE"])
def delete_planet_favorite(planet_id):
    delete_favorite = FavoritePlanets.query.filter_by(id= planet_id).first()

    if delete_favorite is None:
        return jsonify({"msg" : f"Planeta favorito de ID {planet_id} no se encuentrad"}),404

    db.session.delete(delete_favorite)
    db.session.commit()

    return jsonify({"msg" : "Planeta eliminado!"}),200



# [DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.
@app.route('/favorite/people/<int:people_id>',methods= ['DELETE'])
def deletePeople(people_id):
    delete_people = Person.query.filter_by(id = people_id).first()

    if delete_people is None:
        return jsonify({"msg" : "Persona con ID {id} no encontrada"}),404
    
    db.session.delete(delete_people)
    db.session.commit()

    return jsonify({"msg" : "Persona eliminado"}),200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)




