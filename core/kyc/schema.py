from marshmallow import Schema, fields

class MerchantKYCSchema(Schema):
    category_id = fields.Str(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    owner_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)