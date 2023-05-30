from marshmallow import Schema, fields

class CreateStoreSchema(Schema):
    business_name = fields.Str(required=True)
    branch_name = fields.Str(required=True)
    branch_admin = fields.Str(required=True)
    mobile = fields.Str(required=True)
    email = fields.Str(required=True)
    address_1 = fields.Str(required=True)
    address_2 = fields.Str(required=True)
    province = fields.Str(required=True)
    city = fields.Str(required=True)
    barangay = fields.Str(required=True)
    zip = fields.Str(required=True)

class UpdateStoreSchema(Schema):
    business_name = fields.Str(required=False)
    branch_name = fields.Str(required=False)
    branch_admin = fields.Str(required=False)
    mobile = fields.Str(required=False)
    email = fields.Str(required=False)
    address_1 = fields.Str(required=False)
    address_2 = fields.Str(required=False)
    province = fields.Str(required=False)
    city = fields.Str(required=False)
    barangay = fields.Str(required=False)
    zip = fields.Str(required=False)