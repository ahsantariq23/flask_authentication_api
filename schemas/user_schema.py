from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)
