from marshmallow import Schema, fields

class CreateStaffSchema(Schema):
    name = fields.Str(required=True)
    mobile = fields.Str(required=False)
    email = fields.Str(required=True)

class UpdateStaffSchema(Schema):
    name = fields.Str(required=False)
    mobile = fields.Str(required=False)
    email = fields.Str(required=False)