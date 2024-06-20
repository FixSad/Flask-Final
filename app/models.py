from . import db, login_manager, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from authlib.jose import JsonWebSignature
from flask_admin.contrib.sqla import ModelView
from enum import Enum


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    features = db.Column(db.String(150))
    prog_languages = db.Column(db.String(50))
    link = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Project %r>' % self.name


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Company %r>' % self.name


class Role(Enum):
    Admin = 1,
    Moderator = 2,
    Employer = 3,
    Employee = 4


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))
    experience = db.Column(db.Integer)
    city = db.Column(db.String(50))
    role = db.Column(db.Enum(Role))
    projects = db.relationship('Project', backref='user')
    companies = db.relationship('Company', backref='user')
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self):
        if self.role is None:
            self.role = Role.Employee

    def can(self, r):
        return self.role is not None and self.role == r

    def is_admin(self):
        return self.can(Role.Admin)

    @property
    def password(self):
        raise AttributeError('password is not able to read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        print(data)
        if data.payload.decode('utf-8') != str(self.id):
            print('It is not your token')
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    def __repr__(self):
        return '<User %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Project, db.session))