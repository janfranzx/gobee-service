from flask import Blueprint, request, jsonify, Response
from flask_cors import CORS
from bson import objectid, json_util
from .schema import MerchantKYCSchema

from ..auth import validate_token
from ..db import mongo

kyc = Blueprint('kyc', __name__)

@kyc.route('/kyc', methods=['PUT'])
@validate_token
def handle_create_kyc(merchant):
    req_body = request.get_json()
    merchants = mongo.db.merchants
    schema = MerchantKYCSchema()
    errors = schema.validate(req_body)

    try:
        values = req_body
        values['status'] = 'active'
        update_opts = {'$set': req_body}
        

        options = {'_id': merchant['_id']}
        merchants.update_one(options, update_opts)
    except:
        return jsonify({'status': 'error', 'message': 'Could not update merchant'}), 400
    


    return jsonify({'status': 'success'}), 201