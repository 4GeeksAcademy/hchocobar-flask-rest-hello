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
from models import db, Users, Teachers, Students


# Instancias Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
# Configuración de DB
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


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {"message": "Hello, this is your GET /hello response"}
    return jsonify(response_body), 200


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    response_body = {}
    results = []
    if request.method == 'GET':
        # Lógica para consultar la DB y devolver todos los usuarios
        # users = db.session.execute(db.select(Users)).scalars()
        users = db.session.execute(db.select(Users, Teachers, Students)
                          .join(Teachers, Users.id == Teachers.user_id, isouter=True)
                          .join(Students, Users.id == Students.user_id, isouter=True))
        # .scalars() -> una lista de registros, pero como un objeto SQLAlchemy
        # .scalar() -> un registro, pero como un objeto SQLAlchemy
        print(users)
        # response_body['results'] = [row.serialize() for row in users]
        # response_body['message'] = 'Metodo GET de users'
        if users:
            for row in users:
                user, teacher, student = row  # Desestructuación de Python
                # data = {'message': 'Hola', 'nombre': 25}
                data = user.serialize()
                # Utilizo un if en una linea (one-linner)
                # algo = x if x == True else x * 2
                data['profile'] = teacher.serialize() if user.role == 'Teacher' else student.serialize() if user.role == 'Student' else {}
                results.append(data)
            response_body['results'] = results
            return response_body, 200
    if request.method == 'POST':
        data = request.json
        user = Users(email = data['email'],
                     password = data['password'],
                     role = data['role'],
                     is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body['results'] = user.serialize()
        response_body['message'] = 'Metodo POST de users'
        return response_body, 200
        

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    response_body = {}
    print(id)
    if request.method == 'GET':
        response_body['message'] = 'metodo GET del users/<id>'
        return response_body, 200
    if request.method == 'PUT':
        response_body['message'] = 'metodo PUT del users/<id>'
        return response_body, 200
    if request.method == 'DELETE':
        response_body['message'] = 'metodo DELETE del users/<id>'
        return response_body, 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
