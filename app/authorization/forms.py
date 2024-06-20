from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, ValidationError, \
    BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from ..models import User


class RegistrationForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    password_conf = PasswordField("Сonfirm the password: ",
                                  validators=[EqualTo('password', message='Passwords are incorrect'), DataRequired()])
    experience = IntegerField("Experience: ", validators=[DataRequired()])
    city = StringField("City: ", validators=[DataRequired()])
    is_employer = BooleanField("Are you employer?")
    submit = SubmitField("Confirm")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Such mail already exists')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Such name already exists')


class AuthorizationForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Confirm")
