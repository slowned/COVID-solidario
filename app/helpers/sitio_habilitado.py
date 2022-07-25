from app import db
from app.models import Configuracion
from app.resources import sitio_deshabilitado
from flask import render_template, redirect, url_for


def st_habilitado():

    return(Configuracion.sitio_habilitado)


def check_habilitado():

    if not(Configuracion.sitio_habilitado()):
        mensaje = Configuracion.msj_deshabilitado()
        return render_template('/sitio_deshabilitado.html', mensaje=mensaje)
        #redirect(url_for('sitios_deshabilitados.index'))
    else:
        return True
