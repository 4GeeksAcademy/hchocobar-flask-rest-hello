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
from models import db, Users


app = Flask(__name__)
app.url_map.strict_slashes = False
# Config db
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
# Other config
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {"message": "Hello, this is your GET /user response "}
    return jsonify(response_body), 200


""" 
Creamos nuestros endpoints
"""
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        response_body = {}
        results = {}
        users = db.session.execute(db.select(Users)).scalars()
        # Opción 1 - For-in
        list_usuarios = []
        for row in users:
            list_usuarios.append(row.serialize())
        results['users'] = list_usuarios
        # Opción 2 - List Comprehesion
        # results['users'] = [row.serialize() for row in users]
        response_body['message'] = 'Listado de Usuarios'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        # Escribir la lógica para guardar el registro en la DB
        user = Users(email = data.get('email'),
                     password = data.get('password'),
                     is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body['user'] = user.serialize()
        return response_body, 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    response_body = {}
    results = {}
    if request.method == 'GET':
        # opcion 1
        user = db.session.get(Users, user_id)
        if not user:
            response_body['message'] = 'Usuario inexistente'
            return response_body, 404
        """
        # opción 2
        user = db.one_or_404(db.select(Users).filter_by(id=user_id), 
                             description=f"User not found , 404")
        """
        results['user'] = user.serialize()
        response_body['message'] = 'Usuario encontrado'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'Usuario inexistente'
            return response_body, 404        
        user.email = data.get('email')
        db.session.commit()
        results['user'] = user.serialize()
        response_body['message'] = 'Usuario actualizado'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'Usuario inexistente'
            return response_body, 404        
        db.session.delete(user)
        db.session.commit()
        response_body['message'] = 'Usuario eliminado'
        return response_body, 200
    

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
