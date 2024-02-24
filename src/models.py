from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    subscrition_date = db.Column(db.Date)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "email": self.email,
                'is_active': self.is_active,
                'suscription_date': self.subscrition_date}


class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    # 2.2. Atributos del modelo. Tipo de dato(longitud), acepta datos vacíos?, es un dato único?
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    nickname =  db.Column(db.String(20), nullable=False)
    image_url =  db.Column(db.String(120), nullable=False)
    # 2.3. Clave foránea. Tipo de dato, db.ForeignKey('alias.id')
    # 3.3 One to One
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    # 3. Relaciones. db.relationship(Models)
    users = db.relationship(Users)

    def __repr__(self):
        return '<Profile: %r>' % self.firstname

    def serialize(self):
        return {"id": self.id, 
                "firstname": self.firstname,
                "lastname": self.lastname,
                "nickname": self.nickname,
                "image_url": self.image_url,
                "users_id": self.users_id}


class Addresses(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(250))
    street_number = db.Column(db.String(250))
    post_code = db.Column(db.String(250), nullable=False)
    # 3.3 One to Many
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship(Users)


class Characters(db.Model):
    __tablename__ = 'characters'
    # 2. Columnas, 
    # 2.1. Clave primaria. Tipo de dato, primary_key=True
    id = db.Column(db.Integer, primary_key=True)
    # 2.2. Atributos del modelo. Tipo de dato(longitud), acepta datos vacíos?, es un dato único?
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.String)
    hair_color = db.Column(db.String)
    skin_color = db.Column(db.String)
    eye_color = db.Column(db.String)
    birth_year = db.Column(db.String)
    gender = db.Column(db.String)
    homeworld = db.Column(db.String)
    url = db.Column(db.String)


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.Integer)
    terrain = db.Column(db.Integer)
    surface_water = db.Column(db.Integer)
    url = db.Column(db.Integer)


class FavoriteCharacters(db.Model):
    # 1. Creamos el alias de la tabla __tablename__ . Naming convention: snake_case
    __tablename__ = 'favorite_characters'
    # 2. Columnas, 
    # 2.1. Clave primaria. Tipo de dato, primary_key=True
    id = db.Column(db.Integer, primary_key=True)
    # 2.3. Clave foránea. Tipo de dato, db.ForeignKey('alias.id')
    users_id = db.Column(db.Integer, db.ForeignKey('users.id')) # int fk >-< users.id
    characters_id  = db.Column(db.Integer, db.ForeignKey('characters.id'))
    # 3. Relaciones. db.relationship(Models)
    users = db.relationship(Users)
    characters = db.relationship(Characters)


class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    # 3.3 Many to Many
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    users = db.relationship(Users)
    planets = db.relationship(Planets)
