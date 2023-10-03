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
    description = fields.String(required=True)


class UpdateSchema(Schema):
    task_id = fields.String(required=True)
    new_task = fields.Str(required=False)
    status = fields.Str(required=False)
    email = fields.Str(required=False)


class ViewSchema(EmployeeSchema):
    task_id = fields.String(required=True)


class StatusSchema(EmployeeSchema):
    status = fields.Str(required=True)