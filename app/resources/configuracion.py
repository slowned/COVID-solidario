from app.models import Configuracion
from flask import render_template, request, redirect, url_for, session, flash
from . import configuraciones
from app.helpers.auth import authenticated
from app.helpers.auth import has_permission
from app.helpers import handler


@configuraciones.route('/configuracion/index/', methods=['GET'])
def index():
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'config_index'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    return render_template('/configuracion/index.html', config=config)


@configuraciones.route('/configuracion/modify/', methods=['POST'])
def modify():
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if request.method == 'GET':
        return handler.method_error(405)
    if not has_permission((session['current_user']['id']), 'config_update'):
        return handler.unauthorized_error(401)
    nueva_config = request.form.to_dict()
    Configuracion.modify(nueva_config)
    flash("Modificado con exito")
    return redirect(url_for("configuraciones.index"))
    # return render_template('configuraciones.index', config=config, msg=msg)
