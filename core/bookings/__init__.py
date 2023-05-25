from flask import Blueprint, request, jsonify, Response
from bson import objectid, json_util
from datetime import datetime
from .schema import CreateBookingSchema, UpdateBookingSchema
from ..auth import validate_token
from ..db import mongo

bookings = Blueprint('bookings', __name__)

@bookings.route('/bookings', methods=['POST'])
@validate_token
def handle_create_staff(merchant):
    req_body = request.get_json()
    schema = CreateBookingSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    
    staff = mongo.db.staff
    s = {
        'merchant_id': str(merchant['_id']),
        'name': req_body['name'],
        'mobile': req_body['mobile'],
        'email': req_body['email'],
        'status': 'active'
    }
    staff.insert(s)
    response = jsonify({
        'status': 'success',
        'message': 'Successfully inserted staff',
        'data':  req_body
    })

    return response, 201
    
@bookings.route('/bookings/list', methods=['GET'])
@validate_token
def handle_get_all_staff(merchant):
    staff = mongo.db.staff
    s = list(staff.find({'merchant_id': str(merchant['_id'])}))
    # s = json_util.dumps(s)
    resp = {
        'status': 'success',
        'message': 'Successfully retrieved staff',
        'data':  s
    }

    return Response(
        json_util.dumps(resp),
        mimetype='application/json'
    )

    # return response, 200

@bookings.route('/bookings/<booking_id>', methods=['GET'])
@validate_token
def handle_get_staff(merchant, staff_id):
    staff = mongo.db.staff
    s = staff.find_one({'_id': objectid.ObjectId(staff_id)})
    print('!!!!!!!!!!!: ', s)
    if s is None:
        response = jsonify({
            'status': 'error',
            'message': 'Staff does not exist'
        })

        return response, 404

    resp = {
        'status': 'success',
        'message': 'Successfully retrieved staff',
        'data':  s
    }

    return Response(
        json_util.dumps(resp),
        mimetype='application/json'
    )

@bookings.route('/bookings/<booking_id>', methods=['DELETE'])
@validate_token
def handle_delete_staff(merchant, staff_id):
    #check if staff is owned by the requesting merchant
   
    print(str(merchant['_id']))
    staff = mongo.db.staff
    s = staff.find_one({'_id': objectid.ObjectId(staff_id)})
    if str(merchant['_id']) == s['merchant_id']:
        s['deleted_at'] = datetime.now()
        update_opts = {'$set': s}
        options = {'_id': s['_id']}
        staff.update_one(options, update_opts)
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

@bookings.route('/bookings/<booking_id>', methods=['PUT'])
@validate_token
def handle_update_staff(merchant, staff_id):
    req_body = request.get_json()
    schema = UpdateBookingSchema()
    errors = schema.validate(req_body)
    if errors:
        response = jsonify({
            'status': 'error',
            'message': errors
        })

        return response, 404
    
    keys = list(req_body.keys())
    values = list(req_body.values())
    updates = dict()
    for i in range(len(keys)):
        updates = {
            keys[i]: values[i]
        }

    print(updates)
    staff = mongo.db.staff

    try:
        update_opts = {'$set': updates}
        options = {'_id': objectid.ObjectId(staff_id)}
        staff.update_one(options, update_opts)
    except:
        return jsonify({'status': 'error', 'message': 'Could not update staff'}), 400
    
    response = jsonify({
        'status': 'success',
        'message': 'Successfully inserted staff'
    })

    return response, 201



