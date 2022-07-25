from wtforms import (
    Form,
    BooleanField,
    StringField,
    validators,
    IntegerField,
    ValidationError
)
import wtforms_json
wtforms_json.init()
import requests
import json

__all__ = ['CreateCenterForm', 'UpdateCenterForm', 'CreateCenterApiForm', 'FilterTurnApiForm', 'CreateTurnFormApi' ]


def validate_char(form, field):
    if any(char.isdigit() for char in field.data):
        raise validators.ValidationError('No se permiten numeros en el campo')


def validate_hour_field(form, field):
    if field.data < form.open_hour.data:
        raise validators.ValidationError("El horario de cierre del centro debe ser mayor al horario de apertura.")


class CreateCenterForm(Form):
    name = StringField('nombre', [validators.DataRequired(message='Este es un campo requerido')])
    address = StringField('direccion', [validators.DataRequired(message='Este es un campo requerido')])
    phone = StringField('telefono', [validators.DataRequired(message='Este es un campo requerido')])
    open_hour = StringField('hora_apertura', [validators.DataRequired(message='Este es un campo requerido')])
    close_hour = StringField('hora_cierre', [validators.DataRequired(message='Este es un campo requerido'), validate_hour_field])
    township = StringField('municipio', [validators.DataRequired(message='Este es un campo requerido')])
    web_site = StringField('web', [validators.Optional()])
    email = StringField('email', [validators.Email(), validators.Optional()])
    #status = BooleanField('status')
    #view_protocol = StringField('view_protocol')
    lat = StringField('lat', [validators.DataRequired(message='Este es un campo requerido')])
    lng = StringField('long', [validators.DataRequired(message='Este es un campo requerido')])
    #publish = StringField('publish', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    center_type = StringField('tipo_centro', [validators.DataRequired(message='Este es un campo requerido')])


class UpdateCenterForm(Form):
    name = StringField('nombre', [validators.DataRequired(message='Este es un campo requerido')])
    address = StringField('direccion', [validators.DataRequired(message='Este es un campo requerido')])
    phone = StringField('telefono', [validators.DataRequired(message='Este es un campo requerido')])
    open_hour = StringField('hora_apertura', [validators.DataRequired(message='Este es un campo requerido')])
    close_hour = StringField('hora_cierre', [validators.DataRequired(message='Este es un campo requerido')])
    township = StringField('municipio', [validators.DataRequired(message='Este es un campo requerido')])
    web_site = StringField('web', [validators.Optional()])
    email = StringField('email', [validators.Email(), validators.Optional()])
    #status = BooleanField('status')
    #view_protocol = StringField('view_protocol')
    lat = StringField('lat', [validators.DataRequired(message='Este es un campo requerido')])
    lng = StringField('long', [validators.DataRequired(message='Este es un campo requerido')])
    #publish = StringField('publish', [validators.DataRequired(message='Este es un campo requerido'), validate_char])
    center_type = StringField('tipo_centro', [validators.DataRequired(message='Este es un campo requerido')])


class CreateCenterApiForm(Form):
    nombre = StringField('nombre', [validators.DataRequired(message='Este es un campo requerido')])
    direccion = StringField('direccion', [validators.DataRequired(message='Este es un campo requerido')])
    telefono = StringField('telefono', [validators.DataRequired(message='Este es un campo requerido')])
    hora_apertura = StringField('hora_apertura', [validators.DataRequired(message='Este es un campo requerido')])
    hora_cierre = StringField('hora_cierre', [validators.DataRequired(message='Este es un campo requerido')])
    web = StringField('web', [validators.URL(), validators.Optional()])
    email = StringField('email', [validators.Email(), validators.Optional()], default='')
    #tipo = StringField('tipo', [validators.Optional()])
    # campos por defecto
    #township = IntegerField('township', default="Hola Mundo")
    #status = BooleanField('status')
    #view_protocol = StringField('view_protocol', default="No disponible")
    #lat = StringField('lat', default="0.0")
    #lng = StringField('long', default="0.0")
    #publish = StringField('long', [validators.DataRequired(message='Este es un campo requerido'), validate_char])

    # Agregados para actividad 6
    #lat = StringField('lat', [validators.Optional()], default='')
    lat = StringField('lat', [validators.DataRequired(message='Este es un campo requerido')])
    lng = StringField('long', [validators.DataRequired(message='Este es un campo requerido')])
    g_recaptcha_response = StringField('g_recaptcha_response', [validators.InputRequired(message='Campo requerido')])
    tipo = StringField('tipo', [validators.DataRequired(message='Este es un campo requerido')])
    municipio = StringField('municipio', [validators.DataRequired(message='Este es un campo requerido')])


    # JSON REQUEST --- DES SERIALIZAR....
    def validate_g_recaptcha_response(form, g_recaptcha_response):
        payload = {
            "secret": "6LdnLP8ZAAAAAKP90lPplFbHJSgrP4sWxpcvMANl", #Required. The shared key between your site and reCAPTCHA.
            "response": form.g_recaptcha_response.data  #Required. The user response token provided by the reCAPTCHA client-side integration on your site.
            #'remoteip':'127.0.0.1'   #Optional. The user's IP address.
        }
        #import ipdb; ipdb.set_trace()
        json_payload = json.dumps(payload)
        google_response = requests.post("https://www.google.com/recaptcha/api/siteverify", json=json_payload)
        result = json.loads(google_response.text)
        return result['success'], result['error-codes']
    #

class FilterTurnApiForm(Form):
    email = StringField('email', [validators.Email(), validators.Optional()], default='')
    phone = StringField('telefono', [validators.DataRequired(message='Este es un campo requerido')])
    turn = StringField('turno', [validators.DataRequired(message='Este es un campo requerido')])
    date = StringField('dia', [validators.DataRequired(message='Este es un campo requerido')])


class CreateTurnFormApi(Form):
    email_donante = StringField('email_donante', [validators.Email(), validators.DataRequired(message='Campo requerido')])
    telefono_donante = StringField('telefono_donante', [validators.DataRequired(message='Este es un campo requerido')])
    fecha = StringField('fecha', [validators.DataRequired(message='Este es un campo requerido')])
    centro_id = IntegerField('centro_id', [validators.DataRequired(message='Este es un campo requerido')])
    hora_inicio = StringField('hora_inicio', [validators.DataRequired(message='Este es un campo requerido')])
    hora_fin = StringField('hora_fin', [validators.DataRequired(message='Este es un campo requerido')])

    def validate_hora_fin(form, hora_fin):
        if hora_fin.data < form.hora_inicio.data :
            raise ValidationError(message='End date must not be earlier than start date')
