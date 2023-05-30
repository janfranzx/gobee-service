from flask import Blueprint, request, jsonify, Response
from bson import objectid, json_util
from datetime import datetime
from .schema import CreateBookingSchema, UpdateBookingSchema
from ..auth import validate_token
from ..db import mongo

bookings = Blueprint('bookings', __name__)

@bookings.route('/bookings', methods=['POST'])
@validate_token
def handle_create_service(merchant):
    req_body = request.get_json()
    schema = CreateBookingSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    
    bookings = mongo.db.bookings
    s = {
        'merchant_id': str(merchant['_id']),
        'name': req_body['name'],
        'price': req_body['price'],
        'details': req_body['details'],
        'staff': [],
        'status': 'active'
    }
    bookings.insert(s)
    response = jsonify({
        'status': 'success',
        'message': 'Successfully saved service',
        'data':  req_body
    })

    return response, 201
    
@bookings.route('/bookings/list', methods=['GET'])
@validate_token
def handle_get_all_service(merchant):
    bookings = mongo.db.bookings
    s = list(bookings.find({'merchant_id': str(merchant['_id'])}))
    # s = json_util.dumps(s)
    resp = {
        'status': 'success',
        'message': 'Successfully retrieved bookings',
        'data':  s
    }

    return Response(
        json_util.dumps(resp),
        mimetype='application/json'
    )

    # return response, 200

@bookings.route('/bookings/<service_id>', methods=['GET'])
@validate_token
def handle_get_service(merchant, service_id):
    bookings = mongo.db.bookings
    s = bookings.find_one({'_id': objectid.ObjectId(service_id)})
    
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

@bookings.route('/bookings/<service_id>', methods=['DELETE'])
@validate_token
def handle_delete_service(merchant, service_id):
    #check if staff is owned by the requesting merchant
    bookings = mongo.db.bookings
    s = bookings.find_one({'_id': objectid.ObjectId(service_id)})
    if str(merchant['_id']) == s['merchant_id']:
        s['deleted_at'] = datetime.now()
        update_opts = {'$set': s}
        options = {'_id': s['_id']}
        bookings.update_one(options, update_opts)
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

@bookings.route('/bookings/<service_id>', methods=['PUT'])
@validate_token
def handle_update_staff(merchant, service_id):
    req_body = request.get_json()
    schema = UpdateBookingSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    bookings = mongo.db.bookings
    s = bookings.find_one({'_id': objectid.ObjectId(service_id)})
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
        bookings.update_one(options, update_opts)
    except:
        return jsonify({'status': 'error', 'message': 'Could not update staff'}), 400
    
    response = jsonify({
        'status': 'success',
        'message': 'Successfully updated service'
    })

    return response, 201



