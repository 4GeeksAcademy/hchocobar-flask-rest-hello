from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    role = db.Column(db.Enum('Teacher', 'Student', name='role'), nullable=False)

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "email": self.email,
                'is_active': self.is_active,
                'role': self.role}


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    users = db.relationship('Users')

    def __repr__(self):
        return f'<Teacher: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                'user_id': self.user_id}


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    users = db.relationship('Users')

    def __repr__(self):
        return f'<Student: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                'user_id': self.user_id}


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Character: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Planet: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}


class CharacterFavorites(db.Model):
    __tablename__ = 'character_favorites'
    id = db.Column(db.Integer, primary_key=True)
    # Columns FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    # Relationships
    users = db.relationship('Users', foreign_keys=[user_id])
    characters = db.relationship('Characters', foreign_keys=[character_id])

    def __repr__(self):
        return f'<Favorites: {self.id} - User: {self.user_id} - Character: {self.character_id}>'

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                'character_id': self.character_id}


class PlanetFavorites(db.Model):
    __tablename__ = 'planet_favorites'
    id = db.Column(db.Integer, primary_key=True)
    # Columns FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # Relationships
    users = db.relationship('Users', foreign_keys=[user_id])
    planets = db.relationship('Planets', foreign_keys=[planet_id])

    def __repr__(self):
        return f'<Favorites: {self.id} - User: {self.user_id} - Planet: {self.planet_id}>'

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                'planet_id': self.planet_id}
