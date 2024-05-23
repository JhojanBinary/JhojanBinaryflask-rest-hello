from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)



    #nos muestra el resultado cuando hacemos print
    def __repr__(self):
        return 'Usuario con email: {}'.format(self.email)


    #convierte la clase a diccionario
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),unique = True, nullable = False)
    population = db.Column(db.Integer, nullable = False)


    #cuando hacemos print 
    def __repr__(self) :
        return f"Planet {self.id} {self.name}"

        
    #convertir de clase a diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population
        }



class FavoritePlanets(db.Model):
    __tablename__ = "favorite_planets"
    id = db.Column(db.Integer, primary_key = True)
    #FOREIGNKEYS
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)
    user_id_relationship = db.relationship(User)

    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable = False)
    planet_id_relationship = db.relationship(Planets)


    def __repr__(self):
        return f"Al usuario le gusta el planeta {self.planet_id}"
    
    def serialize(self):
        return{
            "id" : self.id,
            "user_id": self.user_id,
            "planet_id" :  self.planet_id
        }
class Person(db.Model):
    __tablename__ = "person" 
    id = db.Column(db.Integer,primary_key = True)
    account = db.Column(db.Integer, nullable = False)
    apell = db.Column(db.String(50), nullable = False)
    name = db.Column (db.String(50), nullable = False)

    def __repr__(self):
        return f"usuario con el id {self.id}"
    
    def serialize(self):
        return{
            "id" : self.id,
            "account" : self.account,
            "apell" : self.apell,
            "name" : self.name
        }


class Addres(db.Model):
    __tablename__ = "addres"
    id = db.Column(db.Integer, primary_key = True)
    person_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Datos de usuarios: {self.id}"
    
    def serialize(self):
        return{
            "id" : self.id,
            "person_id" : self.person_id,
            "user_id" : self.user_id
        }