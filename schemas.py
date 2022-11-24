from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields


class UserToCreate(Schema):
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj),
        load_only=True
    )
    #notes_count = fields.Integer()


class UserData(Schema):
    id = fields.Integer()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()
    notes_count = fields.Integer()


class UserToShow(Schema):
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    notes_count = fields.Integer()


class NoteToUpdate(Schema):
    title = fields.String()
    content = fields.String()
    tags = fields.String()


class NoteByTitle(Schema):
    title = fields.String()


class NoteByTag(Schema):
    tag = fields.String()


class NoteNoId(Schema):
    title = fields.String()
    content = fields.String()
    tags = fields.String()
    user_iduser = fields.Integer()


class NoteData(Schema):
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    tags = fields.String()
    user_iduser = fields.Integer()


class AccessData(Schema):
    user_id = fields.Integer()
    note_id = fields.Integer()
    time = fields.DateTime()


class AccessToCreate(Schema):
    user_id = fields.Integer()


class ChangeNoId(Schema):
    user_id = fields.Integer()
    note_id = fields.Integer()
    time = fields.DateTime()


class TagNoId(Schema):
    tag = fields.String()
