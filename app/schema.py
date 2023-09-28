from marshmallow import Schema, fields


class UserSchema(Schema):
    user_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    confirm_password = fields.String(required=True)
    role = fields.String(required=True)


class LoginSchema(Schema):
    user_name = fields.String(required=True)
    email = fields.String(required=True)


class TaskSchema(Schema):
    user_name = fields.String(required=True)
    email = fields.String(required=True)
    task = fields.String(required=True)
    due_date = fields.String(required=True)


class UpdateSchema(Schema):
    email = fields.String(required=True)
    task = fields.String(required=True)
    
