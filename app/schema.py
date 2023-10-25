from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    email = fields.Email(required=True)
    user_name = fields.String(required=True)


class LoginSchema(EmployeeSchema):
    password = fields.String(required=True)
    user_name = fields.String(required=False)


class UserSchema(LoginSchema, EmployeeSchema):
    confirm_password = fields.String(required=True)
    user_name = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class TaskSchema(Schema):
    task_description = fields.String(required=True)
    due_date = fields.String(required=True)
    user_id = fields.List(fields.String, required=True)
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


class OrgnizationSchema(UserSchema):
    gst_number = fields.String(required=True)
    email = fields.Email(required=False)
    address = fields.String(required=True)
    pincode = fields.String(required=True)
    state = fields.String(required=True)
    country = fields.String(required=True)
    confirm_password = fields.String(required=False)
    technology = fields.List(fields.String, required=True)
    user_name = fields.String(required=False)


# first_name = fields.String(required=False)
# last_name = fields.String(required=False)


class getInfoSchema(EmployeeSchema):
    user_name = fields.String(required=True)
    organization_name = fields.String(required=True)


class SendTaskSchema(Schema):
    task_description = fields.String(required=True)
    organization_name = fields.String(required=True)
