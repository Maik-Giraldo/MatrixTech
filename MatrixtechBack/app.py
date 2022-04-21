from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import random
from schema import schema, schemas

from model import Users, db

app = Flask(__name__)
app.secret_key = ''.join(random.choice(
    f"{string.ascii_uppercase}{string.punctuation}{string.ascii_letters}")for i in range(20))

# Settings for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{'root'}:{'password'}@{'localhost'}/{'users'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS settings
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"],
        }
    },
)

# Obtener usuarios
@app.route('/users', methods=['GET'])
def usersGET():
    if request.method == 'GET':
        users = Users.query.all()

        return jsonify(schemas.dump(users))


# Agregar usuarios
@app.route('/users', methods=['POST'])
def usersPOST():
    if request.method == 'POST':
        new_user = Users(**request.json)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(schema.dump(new_user))


# Actualizar usuarios
@app.route('/users/<id>', methods=['PUT'])
def usersPUT(id=None):
    if request.method == 'PUT':
        user = Users.query.get(id)

        if not user:
            return jsonify({
                'error': 'user not found'
            }), 400

        update_user = request.json

        user.name = update_user['name']
        user.last_name = update_user['last_name']
        user.email = update_user['email']
        user.phone_number = update_user['phone_number']
        user.city = update_user['city']
        user.country = update_user['country']

        db.session.commit()

        return jsonify(schema.dump(user))


#Borrar usuarios
@app.route('/users/<id>', methods=['DELETE'])
def usersDELETE(id=None):
    if request.method == 'DELETE':
        user = Users.query.get(id)

        if not user:
            return jsonify({
                'error': 'user not found'
            }), 400

        db.session.delete(user)

        db.session.commit()

        return jsonify({
            'deleted': True
        }), 400


with app.test_request_context():
    db.init_app(app)
    db.create_all()

app.run(debug=True)
