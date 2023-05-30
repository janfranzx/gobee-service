from flask import Blueprint, request, jsonify
from bson import json_util, objectid
from functools import wraps
from bson import objectid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from .schema import LoginSchema, RegisterSchema
from ..db import mongo
from ..settings import SALT

auth = Blueprint('auth', __name__)

def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        try:
            token_encoded = str.encode(token)
            # print(token_encoded)
            data = jwt.decode(token_encoded, SALT, algorithms=['HS256'])
            print('&&&&&&&&&: ', data)
            merchant = mongo.db.merchants.find_one({'_id': objectid.ObjectId(data['id'])})
            print('**************: ', merchant)
        except Exception as e:
            print(e)
            return jsonify({'status': 'error', 'message': 'invalid token'})
        
        return f(merchant, *args, **kwargs)
    return decorator

@auth.route('/login', methods=['POST'])
def handle_login():
    login_schema = LoginSchema()
    req_body = request.get_json()
    print(req_body)
    errors = login_schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': 'Invalid email and/or password'
        })

        return response, 401
    
    merchants = mongo.db.merchants
    filter = {'email': req_body['email']}
    m = merchants.find_one(filter)
    if not m:
        response = jsonify({'status': 'error', 'message': 'Invalid email and/or password.'})
        return response, 401

    if check_password_hash(m['password'], req_body['password']):
        claims = m
        claims['id'] = str(claims['_id'])
        del claims['_id']
        del claims['password']
        claims['expiry'] = str(datetime.utcnow() + timedelta(days=30))
        token = jwt.encode(claims, SALT)
        return jsonify({'status': 'success', 'token': token})
    
@auth.route('/register', methods=['POST'])
def handle_register():
    schema = RegisterSchema()
    req_body = request.get_json()
    print(req_body)
    errors = schema.validate(req_body)
    if errors:
        print('errors: ', errors)
        response = jsonify({
            'status': 'error',
            'message': 'Could not register merchant.'
        })
        return response, 401
    merchants = mongo.db.merchants
    filter = {'email': req_body['email']}
    print("!!!!: ", req_body['email'])
    m = merchants.find_one(filter)
    if m:
        response = jsonify({
            'status': 'error',
            'message': 'Could not register merchant.'
        })
        return response, 401
    
    pass_hash = generate_password_hash(req_body['password'])
    m = {
        'email': req_body['email'],
        'password': pass_hash,
        'category_id': None,
        'name': None,
        'address': None,
        'owner_name': None,
        'service_hours': None,
        'status': 'setup',
        'username': None,
        'services': None
    }
    print(m)
    merchant_id = str(merchants.insert_one(m).inserted_id)
    m['id'] = str(merchant_id)
    del m['_id']
    del m['password']
    claims = m
    claims['expiry'] = str(datetime.utcnow() + timedelta(days=30))
    token = jwt.encode(claims, SALT)
    response = jsonify({'status': 'success', 'token': token})
    return response, 201