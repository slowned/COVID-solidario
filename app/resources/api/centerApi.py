import datetime
from flask import (
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session,
    json,
    jsonify
)
from sqlalchemy import or_
from app.models.center import Center, Center_type
from app.models.center import Turn
from app.models.configuracion import Configuracion
from app.forms.centers import CreateCenterApiForm
from app.forms.centers import CreateTurnFormApi
from . import centers_api
from app.helpers.auth import authenticated
from app.helpers.auth import has_permission
from app.helpers import handler
from app.helpers.auth import is_not_admin

__all__ = ['show', 'index', 'create']


""" Cool Foo-Bar route.
---
get:
    summary: Foo-Bar endpoint.
    description: Get a single foo with the bar ID.
    parameters:
        - name: bar_id
          in: path
          description: Bar ID
          type: integer
          required: true
    responses:
        200:
            description: Foo object to be returned.
            schema: FooSchema
        404:
            description: Foo not found.
"""

#   http://localhost:5000/centros/1
@centers_api.route('/centros/<int:center_id>', methods=['GET'])
def show(center_id, permiso=''):
    """ Retorna el Centro solicitado como parámetro en la URL
    :param center_id: El ID del Centro a mostrar.
    :type center_id: integer
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json response, status code
    :raises: AttributeError, KeyError
    """
    center = Center.find_by_id(int(center_id))
    status_code = 200
    if not center:
        status_code = 404
        return jsonify(), status_code
    if  center.status == False or center.publish != "Aceptado":
        status_code = 500
        return jsonify(), status_code
    else:    
        center = center.serialize
        return jsonify(atributos=center), status_code

#   http://localhost:5000/centros?page=1
@centers_api.route('/centros', methods=['GET'], defaults={'page': 1})
def index(page, permiso=''):
    """ Retorna el listado de centros paginado según configuracion.
    :param page: Número de página del listado de centros a mostrar
    :type page: int
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json -- the return code
    :raises: AttributeError, KeyError
    """
    param = request.args.get('page')
    if param:
        page = int(param)
    config = Configuracion.query.first()
    centers = Center.filter_enabled_all()
    centers = centers.paginate(page, int(config.elementos_cantidad), False)
    centros = [i.serialize for i in centers.items]
    # Respuestas
    status_code = 200
    if not centros or page > centers.pages:
        status_code = 500
    # Navegabilidad    
    # paginas_totales=centers.pages
    # siguiente= page + 1 if page <= paginas_totales else None
    # anterior= page - 1 if page > 1 else None
    # pagina_siguiente= "Null" if siguiente is None else url_for("centers_api.index", pages=siguiente, _external=True) 
    # pagina_anterior= "Null" if anterior is None else url_for("centers_api.index", pages=anterior, _external=True)
    return jsonify(
                centros=centros, 
                total_centros=centers.total, 
                total_paginas=centers.pages, 
                pagina=page,
                # pagina_siguiente=pagina_siguiente, 
                # pagina_anterior=pagina_anterior
                ), status_code

@centers_api.route('/centros', methods=['POST'])
def create(permiso=""):
    """ Crea un nuevo Centro de Ayuda con los datos en formato JSON del cuerpo de la petición POST
    :param payload?: Json payload to submit
    :type name: string
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json -- the return code
    :raises: AttributeError, KeyError
    """
    """
    # DESCOMENTAR PARA LA ENTREGA....
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_new'):
        return handler.unauthorized_error(401)
    """
    status_code = 200
    form = CreateCenterApiForm.from_json(request.get_json())
    config = Configuracion.query.get(1)
    if form.validate():
        center, value = Center.api_create(form)
        if not center:
            status_code = 500
            #error_message = "DB Insert Failed" + str(value)
        else:
            status_code = 201
            return jsonify(atributos=center.serialize), status_code
    else:
        status_code = 400
        #error_message = "Form Validation Failed"
    # Comentar los error_messages para la entrega    
    return jsonify(
                #error_message=error_message, 
                error=form.errors
                ), status_code


@centers_api.route('/centros/<int:center_id>/turnos_disponibles/', methods=["GET"])
def turnos_disponibles(center_id):
    """
    retorna todos los turnos disponibles para un centro dado
    @params:
        center_id
    """
    status_code = 200
    center = Center.query.filter_by(id=center_id).first()
    date = request.args.get('fecha', datetime.datetime.today().date())
    if center:
        turns = Turn.get_turns(center.id, date, True)
        serialized_turns = center.serialize_available_turns(turns=turns, date=date)
        return jsonify(serialized_turns), status_code
    else:
        status_code = 500
        error_message = "Internal Server Error"
    return jsonify(error_message=error_message), status_code


@centers_api.route('/centros/<int:center_id>/reserva/', methods=["POST"])
def reserva(center_id):
    """
    registra un turno para un usuario
    @params:
        center_id
        fecha
        hora_inicio
        hora_fin
        email_donante
        telefono_donante
    """
    status_code = 200
    data = request.get_json()
    form = CreateTurnFormApi.from_json(data)
    if form.validate():
        center = Center.query.filter_by(id=center_id).first_or_404()
        turn = Turn.get_turn_by_datetime(
            center.id, form.fecha.data, form.hora_inicio.data)
        if not turn:
            status_code = 500
            error_message = "Internal Server Error"
        else:
            turn = turn.assing_user_api(form)
            status_code = 201
            return jsonify(atributos=turn.serialize_turns), status_code
    else:
        status_code = 400
        error_message = "Bad request"
    return jsonify(error_message=error_message, error=form.errors), status_code


@centers_api.route('/centros/tipos', methods=["GET"])
def tipos_centro():
    status_code=200
    tipos = Center_type.all()
    lista_tipos = [i.serialize for i in tipos]
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify(tipos=lista_tipos), status_code

# retorna todos los centros sin paginar
@centers_api.route('/centros/all', methods=['GET'])
def cetros_all():
    """ Retorna el listado de centros paginado según configuracion.
    :param page: Número de página del listado de centros a mostrar
    :type page: int
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json -- the return code
    :raises: AttributeError, KeyError
    """
    centers = Center.filter_enabled_all()
    centros = [i.serialize for i in centers]
    # Respuestas
    status_code = 200
    if not centros :
        status_code = 500
    # Navegabilidad    
    # paginas_totales=centers.pages
    # siguiente= page + 1 if page <= paginas_totales else None
    # anterior= page - 1 if page > 1 else None
    # pagina_siguiente= "Null" if siguiente is None else url_for("centers_api.index", pages=siguiente, _external=True) 
    # pagina_anterior= "Null" if anterior is None else url_for("centers_api.index", pages=anterior, _external=True)
    return jsonify(
                centros=centros 
                #total_centros=centers.total, 
                #total_paginas=centers.pages, 
                #pagina=page,
                # pagina_siguiente=pagina_siguiente, 
                # pagina_anterior=pagina_anterior
                ), status_code


# cantidad de centros por tipo
@centers_api.route('/tiposCentro', methods=['GET'])
def stat_tiposCentro():
    """ Retorna el listado de centros paginado según configuracion.
    :param page: Número de página del listado de centros a mostrar
    :type page: int
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json -- the return code
    :raises: AttributeError, KeyError
    """
    centers = Center.filter_enabled_all()
    centers = Center.centers_by_type()
    
    centros = ("Tipo de centro", "Cantidad")
    
    # Respuestas
    status_code = 200
    if not centers:
        status_code = 500
    # Navegabilidad    
    # paginas_totales=centers.pages
    # siguiente= page + 1 if page <= paginas_totales else None
    # anterior= page - 1 if page > 1 else None
    # pagina_siguiente= "Null" if siguiente is None else url_for("centers_api.index", pages=siguiente, _external=True) 
    # pagina_anterior= "Null" if anterior is None else url_for("centers_api.index", pages=anterior, _external=True)
    #return centers
    return jsonify(
        centros=centers
                #total_centros=centers.total, 
                #total_paginas=centers.pages, 
                #pagina=page,
                # pagina_siguiente=pagina_siguiente, 
                # pagina_anterior=pagina_anterior
        ), status_code


# cantidad de centros por localidad
@centers_api.route('/estadisticas/centros/por/localidad', methods=['GET'])
def stat_centros_por_localidad():
    """ Retorna el listado de centros paginado según configuracion.
    :param page: Número de página del listado de centros a mostrar
    :type page: int
    :param permiso: El permiso asociado, necesario para acceder (optional, default: None)
    :type permiso: string
    :returns: json -- the return code
    :raises: AttributeError, KeyError
    """
    
    #centers = Center.filter_enabled_all()
    stats = Center.centers_by_township()

        # Respuestas
    status_code = 200
    if not stats:
        status_code = 500
    return jsonify(
        stats=stats
        ), status_code


@centers_api.route('/estadisticas/turnos-concurridos/', methods=['GET'])
def recurrent_turn_stats():
    recurrents_turns = Turn.recurrent_turn_stats()
    status_code = 200
    if not recurrents_turns:
        status_code = 500
    serialized_turns = [Turn.serialize_turn_stats(turn) for turn in recurrents_turns]

    # serializar
    return jsonify(turns=serialized_turns), status_code
