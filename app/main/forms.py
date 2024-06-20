from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    features = StringField("Features: ")
    prog_languages = StringField("Programming languages: ")
    link = StringField("Link: ")
    submit = SubmitField("Add")


class CompanyForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    submit = SubmitField("Add")