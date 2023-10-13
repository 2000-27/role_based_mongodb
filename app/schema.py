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
    company_name = fields.String(required=True)


class TaskSchema(EmployeeSchema):
    task_description = fields.String(required=True)
    due_date = fields.String(required=True)
    user_name = fields.String(required=False)
    rate = fields.Integer(required=True)


class InfoSchema(EmployeeSchema):
    task_id = fields.String(required=True)
    user_name = fields.String(required=False)
    email = fields.Email(required=False)


class UpdateSchema(Schema):
    task_id = fields.String(required=True)
    task_description = fields.Str(required=False)
    status = fields.Str(required=False)
    email = fields.Email(required=False)


class ViewSchema(EmployeeSchema):
    task_id = fields.String(required=True)
    user_name = fields.String(required=False)
    email = fields.Email(required=False)


class StatusSchema(Schema):
    status = fields.Str(required=True)
    task_id = fields.String(required=True)
    time_needed = fields.Integer(required=True)
