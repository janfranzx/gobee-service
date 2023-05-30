from flask import Blueprint, request, jsonify, Response
from bson import objectid, json_util
from datetime import datetime
from .schema import CreateStoreSchema, UpdateStoreSchema
from ..auth import validate_token
from ..db import mongo

stores = Blueprint('stores', __name__)

@stores.route('/stores', methods=['POST'])
@validate_token
def handle_create_store(merchant):
    print('!!!!!!!', merchant)
    req_body = request.get_json()
    schema = CreateStoreSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    
    stores = mongo.db.stores
    s = req_body
    s['merchant_id'] = str(merchant['_id'])
    stores.insert(s)
    response = jsonify({
        'status': 'success',
        'message': 'Successfully saved service',
        'data':  req_body
    })

    return response, 201
    
@stores.route('/stores/list', methods=['GET'])
@validate_token
def handle_get_all_store(merchant):
    stores = mongo.db.stores
    s = list(stores.find({'merchant_id': str(merchant['_id'])}))
    # s = json_util.dumps(s)
    resp = {
        'status': 'success',
        'message': 'Successfully retrieved stores',
        'data':  s
    }

    return Response(
        json_util.dumps(resp),
        mimetype='application/json'
    )

    # return response, 200

@stores.route('/stores/<store_id>', methods=['GET'])
@validate_token
def handle_get_service(merchant, service_id):
    stores = mongo.db.stores
    s = stores.find_one({'_id': objectid.ObjectId(service_id)})
    
    if s is None:
        response = jsonify({
            'status': 'error',
            'message': 'Service does not exist'
        })

        return response, 404
    
    if str(merchant['_id']) != s['merchant_id']:
        response = jsonify({
            'status': 'error',
            'message': 'Unauthorized'
        })

        return response, 403

    resp = {
        'status': 'success',
        'message': 'Successfully retrieved service',
        'data':  s
    }

    return Response(
        json_util.dumps(resp),
        mimetype='application/json'
    )

@stores.route('/stores/<store_id>', methods=['DELETE'])
@validate_token
def handle_delete_service(merchant, service_id):
    #check if staff is owned by the requesting merchant
    stores = mongo.db.stores
    s = stores.find_one({'_id': objectid.ObjectId(service_id)})
    if str(merchant['_id']) == s['merchant_id']:
        s['deleted_at'] = datetime.now()
        update_opts = {'$set': s}
        options = {'_id': s['_id']}
        stores.update_one(options, update_opts)
        response = jsonify({
            'status': 'success',
            'message': 'Successfully deleted staff'
        })

        return response, 201

    resp = jsonify({
        'status': 'error',
        'message': 'Failed to delete staff'
    })

    return resp, 400

@stores.route('/stores/<store_id>', methods=['PUT'])
@validate_token
def handle_update_staff(merchant, service_id):
    req_body = request.get_json()
    schema = UpdateStoreSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    stores = mongo.db.stores
    s = stores.find_one({'_id': objectid.ObjectId(service_id)})
    if str(merchant['_id']) != s['merchant_id']:
        response = jsonify({
            'status': 'error',
            'message': 'Unauthorized'
        })

        return response, 403
    
    keys = list(req_body.keys())
    values = list(req_body.values())
    updates = dict()
    for i in range(len(keys)):
        updates = {
            keys[i]: values[i]
        }

    try:
        update_opts = {'$set': updates}
        options = {'_id': objectid.ObjectId(service_id)}
        stores.update_one(options, update_opts)
    except:
        return jsonify({'status': 'error', 'message': 'Could not update staff'}), 400
    
    response = jsonify({
        'status': 'success',
        'message': 'Successfully updated service'
    })

    return response, 201



