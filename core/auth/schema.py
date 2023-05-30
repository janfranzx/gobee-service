from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class MerchantServicesSetupSchema(Schema):
    name = fields.Str(required=True)
    details = fields.Str(required=False)
    price = fields.Float(required=True)
    allow_choosing_personnel = fields.Boolean(required=True)

class MerchantPersonnel(Schema):
    name = fields.Str(required=True)
    schedule = fields.Str(required=True)
    photo_url = fields.Str(required=False)