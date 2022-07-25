from wtforms import (
    Form,
    BooleanField,
    StringField,
    validators,
    IntegerField
)

__all__ = ['RegisterTurn']

class RegisterTurn(Form):
    user_email = StringField('email', [validators.Email(), validators.Optional()], default='')
    user_phone = StringField('telefono', [validators.DataRequired(message='Este es un campo requerido')])
