from flask import render_template
from app import db
from app.models import Configuracion

def not_found_error(e):
    config = Configuracion.all()
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs, config=config), 404


def unauthorized_error(e):
    config = Configuracion.all()
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs, config=config), 401


def method_error(e):
    config = Configuracion.all()
    kwargs = {
        "error_name": "405 Metodo no permitido",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs, config=config), 405
