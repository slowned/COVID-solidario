from flask import render_template
from app.models.configuracion import Configuracion
from . import sitios_deshabilitados


@sitios_deshabilitados.route('/sitios_deshabilitados/index', methods=['GET','POST'])
def index():
    mensaje = Configuracion.msj_deshabilitado()
    config = Configuracion.all()
    return render_template('/sitio_deshabilitado.html', config=config, mensaje=mensaje)
