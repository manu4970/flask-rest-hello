from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

peopleFavs = db.Table("peopleFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("people_id", db.Integer, db.ForeignKey("people.id"), primary_key=True)
)

planetsFavs = db.Table("planetsFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("planets_id", db.Integer, db.ForeignKey("planets.id"), primary_key=True)
)
    
class People(db.Model):
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
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    peopleFav = db.relationship(People,
                    secondary=peopleFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))
    planetsFav = db.relationship(Planets,
                    secondary=planetsFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "people_fav": self.peopleFav,
            "planet_fav": self.planetsFav
            # do not serialize the password, its a security breach
        }