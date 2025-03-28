from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class Recherche(FlaskForm):
    nom_individu = StringField("nom_individu", validators=[])
    nom_bapteme = StringField("nom_bapteme", validators=[])

