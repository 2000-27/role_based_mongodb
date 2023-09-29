from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    email = fields.Email(required=True)
    user_name = fields.String(required=True)


class LoginSchema(EmployeeSchema):
    password = fields.String(required=True)


class UserSchema(LoginSchema, EmployeeSchema):
    confirm_password = fields.String(required=True)
    role = fields.String(required=True)


class TaskSchema(EmployeeSchema):
    task = fields.String(required=True)
    due_date = fields.String(required=True)


class InfoSchema(EmployeeSchema):
    task = fields.String(required=True)
