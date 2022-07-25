from wtforms import (
    Form,
    BooleanField,
    StringField,
    validators,
)

__all__ = ['CreateUserForm' , 'UpdateUserForm']

def validate_char(form, field):
    if any(char.isdigit() for char in field.data):
        raise validators.ValidationError('No se permiten numeros en el campo')

class CreateUserForm(Form):
    name = StringField('Nombre', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    surname = StringField('Apellido', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    user_name = StringField('Nombre de usuario', [validators.InputRequired(message='Campo requerido')])
    email = StringField('Email', [validators.Email(), validators.InputRequired(message='Campo requerido')])
    password = StringField('Password', [validators.InputRequired(message='Campo requerido')])
    active = BooleanField('Activo')
    roles = StringField('Roles', [validators.InputRequired(message='Campo requerido')])

class UpdateUserForm(Form):
    name = StringField('Nombre', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    surname = StringField('Apellido', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    user_name = StringField('Nombre de usuario', [validators.InputRequired(message='Campo requerido')])
    email = StringField('Email', [validators.Email(), validators.InputRequired(message='Campo requerido')])
    active = BooleanField('Activo')
    # roles = StringField('Roles',[validators.InputRequired(message='Campo requerido')])
