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
    description = fields.String(required=True)
    due_date = fields.String(required=True)


class InfoSchema(EmployeeSchema):
    task_descrption = fields.String(required=True)


class UpdateSchema(Schema):
    task_id = fields.String(required=True)
    new_task = fields.Str(required=True)


class UpdateStatus(Schema):
    task_id = fields.String(required=True)
    status = fields.Str(required=True)

