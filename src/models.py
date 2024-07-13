from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    Favorite_people= db.relationship("Favorite_people", backref="user",lazy=True)
    favorite_planets= db.relationship("Favorite_planet", back_populates='user',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(50))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    Favorite_people= db.relationship("Favorite_people", backref="character",lazy=True)
    
    
    def __repr__(self):
        return '<people %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            # do not serialize the password, its a security breach
        }
    
class Favorite_people(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey(User.id))
    people_id =db.Column(db.Integer,db.ForeignKey(People.id))


    def __repr__(self):
        return '<people %r>' % self.id

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "people_id": self.people_id
        }
    

class Planet(db.Model):
    __tablename__= "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population =db.Column(db.Integer,nullable=False)
    climate= db.Column(db.String(250), nullable=False)
    favorite_planets= db.relationship("Favorite_planet",  back_populates='planet',lazy=True)
    
    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }


class Favorite_planet(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey(User.id))
    planet_id =db.Column(db.Integer,db.ForeignKey(Planet.id))

    user = db.relationship('User', back_populates='favorite_planets')
    planet = db.relationship('Planet', back_populates='favorite_planets')

    def __repr__(self):
        return '<planet %r>' % self.id

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "planet_id": self.planet_id
        }