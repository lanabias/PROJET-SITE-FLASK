from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,TextAreaField, SelectMultipleField

class Recherche(FlaskForm):
    nom_individu = StringField("nom_individu", validators=[])
    nom_bapteme = StringField("nom_bapteme", validators=[])

