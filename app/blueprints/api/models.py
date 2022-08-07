from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy import desc
import os
import base64

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(32), index=True)
    token_expiration = db.Column(db.DateTime(), default=datetime.utcnow())
    recipies = db.relationship('Recipe', backref='owner', lazy='dynamic')

    def __init__(self, email=None, username=None, password=None):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User Object | {self.username}>'

    def __str__(self):
        return f'User - {self.id} - {self.username}'

    def get_token(self, expires_in=7200):
        now = datetime.utcnow()
        if self.token and self.token_expiration > (now + timedelta(seconds=60)):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        else:
            return user
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }

    def from_dict(self, data):
        for field in ['email', 'password', 'username']:
            if field in data:
                if field == 'password':
                    setattr(self, field, generate_password_hash(data[field]))
                else:
                    setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    photo = db.Column(db.String(1000), nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description=None, photo=None, user_id=None):
        self.name = name
        self.description = description
        self.photo = photo
        self.user_id = user_id

    def __repr__(self):
        return f'<Recipe Object | {self.name}>'

    def __str__(self):
        return f'Recipe - {self.id} - {self.name}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'photo': self.photo,
            'date_created': self.date_created
        }

    def from_dict(self, data):
        for field in ['name', 'description', 'photo', 'user_id']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    quantity = db.Column(db.String(255), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __init__(self, name, description=None, quantity=None, recipe_id=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.recipe_id = recipe_id

    def __repr__(self):
        return f'<Ingredient Object | {self.name}>'

    def __str__(self):
        return f'Ingredient - {self.id} - {self.name}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity
        }

    def from_dict(self, data):
        for field in ['name', 'description', 'quantity', 'recipe_id']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()