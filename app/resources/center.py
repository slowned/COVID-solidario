from datetime import datetime
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
from werkzeug.utils import secure_filename
from app.forms.centers import CreateCenterForm, UpdateCenterForm
from app.helpers.auth import authenticated
from app.helpers.auth import has_permission
from app.helpers import handler
from app.helpers.auth import is_not_admin
from app.models.center import Center
from app.models.configuracion import Configuracion
from app.models.user import User, Role
from app.models.center import Center, Center_type, Turn
from app.helpers.files import allowed_file
from app.forms.turns import RegisterTurn

from . import centers
from . import configuraciones
from . import turns


__all__ = ['create', 'list', 'delete', 'detail', 'update', 'accept', 'reject']


@centers.route('/center/create', methods=['GET', 'POST'])
def create(permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_new'):
        return handler.unauthorized_error(401)
    tipos_centro = Center_type.query.all()
    form = CreateCenterForm(request.form)
    #form = request.form
    config = Configuracion.query.get(1)
    if request.method == 'POST':
        if form.validate():
       #     flash(form)
            center, _ = Center.create(form)
            file = request.files["view_protocol"]
            if (request.files['view_protocol'].filename != ''):
                path = 'app/static/uploads/'
                filename = str(center.id) + '_' + secure_filename(file.filename)
                file.save(path+filename)
                Center.set_view_protocol(pk=center.id, file=filename)
            flash("Alta exitosa")
            return redirect(url_for('centers.list'))
    msg = "error"
    return render_template('centers/center_create.html', center_types=tipos_centro, form=form, config=config , msg=msg)


@centers.route('/center/list/', methods=['GET', 'POST'], defaults={'page': 1})
@centers.route('/center/list/<int:page>', methods=['GET', 'POST'])
def list(page, permiso=''):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_index'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    page = page
    centros = Center.query.filter_by()
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        publish = form.get('publish')
        if name:
            search = "%{}%".format(name)
            centros = centros.filter(Center.name.like(search))
        if publish:
            #publish = centros.filter(Center.publish.like(publish))
            centros = centros.filter_by(publish=publish)
    config = Configuracion.query.first()
    centros = centros.paginate(page, int(config.elementos_cantidad), False)
    return render_template('centers/center_list.html', center_list=centros, config=config )


@centers.route('/center/delete/<int:center_id>', methods=['POST'])
def delete(center_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_destroy'):
        return handler.unauthorized_error(401)
    session_id = session['current_user']['id']
    Center.delete(center_id)
    flash("Centro eliminado correctamente.")
    return redirect(url_for('centers.list'))


@centers.route('/center/detail/<int:center_id>')
def detail(center_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_show'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    center = Center.query.filter_by(id=center_id).first_or_404()
    return render_template('centers/center_detail.html', center=center, config=config)  


@centers.route('/center/update/<int:center_id>', methods=['GET', 'POST'])
def update(center_id, permiso=""):
    #updatear el formulario y que sean los campos opcionales
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_update'):
        return handler.unauthorized_error(401)
    center = Center.query.filter_by(id=center_id).first_or_404()
    form = UpdateCenterForm(request.form)
    tipos_centro = Center_type.query.all()
    config = Configuracion.query.get(1)
    if request.method == 'POST':
        if form.validate():
            center = center.update(form)
            file = request.files["view_protocol"]
            if (request.files['view_protocol'].filename != ''):
                path = 'app/static/uploads/'
                filename = str(center.id) + '_' + secure_filename(file.filename)
                file.save(path+filename)
                Center.set_view_protocol(pk=center.id, file=filename)
            flash("Modificacion exitosa")
            return redirect(url_for('centers.list'))
    return render_template('centers/center_update.html', center=center, form=form, center_types=tipos_centro, config=config)


@centers.route('/center/accept/<int:center_id>', methods=['POST'])
def accept(center_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_destroy'):
        return handler.unauthorized_error(401)
    session_id = session['current_user']['id']
    Center.accept(center_id)
    flash("Centro aceptado.")
    return redirect(url_for('centers.list'))



@centers.route('/center/reject/<int:center_id>', methods=['POST'])
def reject(center_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'center_destroy'):
        return handler.unauthorized_error(401)
    session_id = session['current_user']['id']
    Center.reject(center_id)
    flash("Centro rechazado.")
    return redirect(url_for('centers.list'))


@centers.route('/center/register_turn/<int:turn_id>', methods=['GET', 'POST'])
def register_turn(turn_id):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_new'):
        return handler.unauthorized_error(401)

    config = Configuracion.query.get(1)
    turn = Turn.query.filter_by(id=turn_id).first_or_404()

    form = RegisterTurn(request.form)
    if request.method == "POST":
        if form.validate():
            turn = turn.assing_user(form)
            return redirect(url_for('turns.detail', turn_id=turn.id))
    return render_template(
        'turns/register.html',
        config=config,
        turn=turn,
        form=form,
    )


@centers.route('/center/available_turns/<int:center_id>', methods=['GET'])
def available_turns(center_id):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_new'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    
    date = request.args.get('date')
    if not date:
        date=datetime.today().date()
    
    
    turns = Turn.get_turns(center_id, date)
    return render_template(
        'centers/available_turns.html',
        turns=turns,
        config=config
    )
