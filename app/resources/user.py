from flask import (
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session
)
from sqlalchemy import or_

from app.models.user import User, Role
from app.models.configuracion import Configuracion
from app.forms.users import CreateUserForm, UpdateUserForm
from . import users
from app.helpers.auth import authenticated
from app.helpers.auth import has_permission
from app.helpers import handler
from . import configuraciones
from app.helpers.auth import is_not_admin

__all__ = ['create']


@users.route('/user/create', methods=['GET', 'POST'])
def create(permiso=""):
    """
        @Params: [name, surname, email, user_name, active, rol[]]
        return: User instance
    """
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_new'):
        return handler.unauthorized_error(401)
    roles = Role.query.all()

    form = CreateUserForm(request.form)
    config = Configuracion.query.get(1)
    if request.method == 'POST':
        if form.validate():
            user = User.filter_by_email_and_username(
                email=form.email.data,
                user_name=form.user_name.data,
            )
            if user:
                msg = "Error al crear usuario: Email o Nombre de usuario ya existente"
                return render_template(
                        'users/create.html',
                        msg=msg,
                        form=form,
                        config=config
                ), 403
            user, _ = User.create(form)
            return redirect(url_for('users.list'))
    return render_template('users/create.html', roles=roles, config=config)


@users.route('/user/delete/<int:user_id>', methods=['POST'])
def delete(user_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_destroy'):
        return handler.unauthorized_error(401)
    session_id = session['current_user']['id']
    if (not (user_id == session_id)):
        User.delete(user_id)
    else:
        flash("No se puede eliminar el usuario logueado")
    return redirect(url_for('users.list'))


@users.route('/user/detail/<int:user_id>')
def detail(user_id, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_show'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('users/detail.html', user=user, config=config)


@users.route('/user/list/', methods=['GET', 'POST'], defaults={'page': 1})
@users.route('/user/list/<int:page>', methods=['GET', 'POST'])
def list(page, permiso=""):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_index'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    page = page
    users = User.query.filter_by()
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        active = form.get('active')
        if name:
            # users = users.filter_by(name=name)
            search = "%{}%".format(name)
            users = users.filter(User.user_name.like(search))
        if active:
            active = True if active == "True" else False
            users = users.filter_by(active=active)
    conf = Configuracion.query.first()
    users = users.paginate(page, int(conf.elementos_cantidad), False)
    return render_template('users/list.html', user_list=users, config=config)


@users.route('/user/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id, permiso=""):
    #updatear el formulario y que sean los campos opcionales
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_update'):
        return handler.unauthorized_error(401)
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UpdateUserForm(request.form)
    config = Configuracion.query.get(1)
    if request.method == 'POST':
        if form.validate():
                user = user.update(form)
                return redirect(url_for('users.list'))
    return render_template('users/update.html', user=user, form=form, config=config)
