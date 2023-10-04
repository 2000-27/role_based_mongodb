from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    email = fields.Email(required=True)
    user_name = fields.String(required=True)


class LoginSchema(EmployeeSchema):
    password = fields.String(required=True)
    user_name = fields.String(required=False)


class UserSchema(LoginSchema, EmployeeSchema):
    confirm_password = fields.String(required=True)
    role = fields.String(required=True)
    user_name = fields.String(required=True)


class TaskSchema(EmployeeSchema):
    description = fields.String(required=True)
    due_date = fields.String(required=True)
    user_name = fields.String(required=False)


class InfoSchema(EmployeeSchema):
    task_id = fields.String(required=True)
    user_name = fields.String(required=False)


class UpdateSchema(Schema):
    task_id = fields.String(required=True)
    description = fields.Str(required=False)
    status = fields.Str(required=False)
    email = fields.Str(required=False)


class ViewSchema(EmployeeSchema):
    task_id = fields.String(required=True)
    user_name = fields.String(required=False)


class StatusSchema(Schema):
    status = fields.Str(required=True)
    task_id = fields.String(required=True)
