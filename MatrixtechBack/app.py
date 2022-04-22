from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import random
from schema import schema, schemas
from os import getenv as env

from utils.jwt_crypt import JwtCrypt
from utils.bcrypt_crypt import BcryptCrypt
from model import Users, db
from utils.upload_dropbox import UploadDropbox

app = Flask(__name__)
app.secret_key = ''.join(random.choice(
    f"{string.ascii_uppercase}{string.punctuation}{string.ascii_letters}")for i in range(20))

# Settings for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{'dbmt'}:{'m3n.3du.n4l'}@{'mysql-dbmt.alwaysdata.net'}/{'dbmt_mysql'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS settings
CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:4200",
            "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)


# Registro usuarios
@app.route('/users/register', methods=['POST'])
def usersRegisterPOST():
    if request.method == 'POST':
        new_user = Users(**request.json)
        verify_email = schemas.dump(Users.query.filter_by(email = new_user.email))

        if verify_email:
            return jsonify({
                "registered": False,
                "message": "email already in use"
            })

        new_user.password = BcryptCrypt().encrypt(new_user.password)
        new_user.img_profile = ''
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "registered": True,
            "message": "user registered"
        })


# Inicio de sesion
@app.route('/users/login', methods=['POST'])
def loginregisterPOST():
    if request.method == 'POST':
        user = request.json
        verify_user = schemas.dump(Users.query.filter_by(email = user.get('email')))

        if not verify_user:
            return jsonify({
                "logged": False,
                "message": "email or password incorrect"
            })

        if not BcryptCrypt().validate(user.get('password'), verify_user[0].get('password')):
            return jsonify({
                "logged": False,
                "message": "email or password incorrect"
            })
        
        jwt = JwtCrypt().encrypt({'user_id': verify_user[0].get('id')})

        return jsonify({
            "logged": True,
            "data": {
                'name': verify_user[0].get('name'),
                'last_name': verify_user[0].get('last_name'),
                'email': verify_user[0].get('email'),
                'img_profile': verify_user[0].get('img_profile'),
                'phone_number': verify_user[0].get('phone_number'),
                'city': verify_user[0].get('city'),
                'country': verify_user[0].get('country'),
            },
            "message": "login success",
            "token": jwt
        })


# Actualizar usuarios
@app.route('/users', methods=['PUT'])
def usersPUT():
    if request.method == 'PUT':
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        if not token:
            return jsonify({
                "updated": False,
                "message": "token not found"
            })

        try:
            user_id = JwtCrypt().decrypt(token)['user_id']
        except:
            return jsonify({
                "updated": False,
                "message": "token invalid"
            })
    
        user = Users.query.get(user_id)

        if not user:
            return jsonify({
                "updated": False,
                'message': 'user not found'
            })

        update_user = request.json

        user.name = update_user['name']
        user.last_name = update_user['last_name']
        user.email = update_user['email']
        user.phone_number = update_user['phone_number']
        user.city = update_user['city']
        user.country = update_user['country']

        if update_user['password']:
            user.password = BcryptCrypt().encrypt(update_user['password'])

        if update_user['img_profile']:
            img_url = UploadDropbox().saveImage(update_user['img_profile'])

            if img_url:
                user.img_profile = img_url
            else:
                return jsonify({
                    "updated": False,
                    "message": "invalid image"
                })
            

        db.session.commit()

        return jsonify({
            "updated": True,
            "data": {
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'img_profile': user.img_profile,
                'phone_number': user.phone_number,
                'city': user.city,
                'country': user.country,
            },
            "message": "user updated"
        })


# Informacion a partir de token
@app.route('/verify_token', methods=['POST'])
def verify_token():
    if request.method == 'POST':
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None

        if not token:
            return jsonify({
                "verified": False,
                "message": "token not found"
            })

        try:
            user_id = JwtCrypt().decrypt(token)['user_id']
        except:
            return jsonify({
                "verified": False,
                "message": "token invalid"
            })
    
        user = Users.query.get(user_id)

        if not user:
            return jsonify({
                "verified": False,
                'message': 'user not found'
            })

        return jsonify({
            "verified": True,
            "data": {
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'img_profile': user.img_profile,
                'phone_number': user.phone_number,
                'city': user.city,
                'country': user.country,
            },
            "message": "token verified"
        })


# Borrar usuarios
@app.route('/users', methods=['DELETE'])
def usersDELETE():
    if request.method == 'DELETE':
        token = request.headers.get('Authorization').split(" ")[1] if request.headers.get('Authorization') else None
        
        if not token:
            return jsonify({
                "deleted": False,
                "message": "token not found"
            })
        
        try:
            user_id = JwtCrypt().decrypt(token)['user_id']
        except:
            return jsonify({
                "deleted": False,
                "message": "token invalid"
            })

        user = Users.query.get(user_id)

        if not user:
            return jsonify({
                'deleted': False,
                'message': 'user not found'
                
            })

        db.session.delete(user)

        db.session.commit()

        return jsonify({
            'deleted': True,
            'message': 'user deleted'
        })
        


# Inicializar app
with app.test_request_context():
    db.init_app(app)
    db.create_all()

app.run(debug=True, port=env('PORT', 5000), host=env('HOST', '0.0.0.0'))
