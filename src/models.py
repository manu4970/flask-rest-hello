from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    personaje = db.relationship("People")
    planeta = db.relationship("Planets")
    usuario = db.relationship("User")

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize2(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.planeta_id,
        }
