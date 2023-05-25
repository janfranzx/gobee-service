from marshmallow import Schema, fields

class LoginSchema(Schema):
    mobile = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterSchema(Schema):
    mobile = fields.Str(required=True)
    password = fields.Str(required=True)

# class MerchantAccountSetupSchema(Schema):
#     category = fields.Str(required=True)
#     name = fields.Str(required=True)
#     address = fields.Str(required=True)
#     owner_name = fields.Str(required=True)
#     service_hours = fields.List(required=True)
#     username = fields.Str(required=True)
#     email = fields.Str(required=True)

class MerchantServicesSetupSchema(Schema):
    name = fields.Str(required=True)
    details = fields.Str(required=False)
    price = fields.Float(required=True)
    allow_choosing_personnel = fields.Boolean(required=True)

class MerchantPersonnel(Schema):
    name = fields.Str(required=True)
    schedule = fields.Str(required=True)
    photo_url = fields.Str(required=False)