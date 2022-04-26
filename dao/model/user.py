from setup_db import db
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)


class UserSchema(Schema):
    """
    Схема сериализации данных модели User.
    """
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
