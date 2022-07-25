from wtforms import (
    Form,
    StringField,
    validators,
)


__all__ = ['CreateLoginForm']

class CreateLoginForm(Form):
    email = StringField('Email', [validators.InputRequired(message='Campo requerido')])
    password = StringField('Password', [validators.InputRequired(message='Campo requerido')])
