from marshmallow import Schema, fields

class CreateServiceSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Decimal(required=True)
    details = fields.Str(required=False)
    staff = fields.List(fields.Str(), required=False)

class UpdateServiceSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Decimal(required=True)
    details = fields.Str(required=False)
    staff = fields.List(fields.Str(), required=False)