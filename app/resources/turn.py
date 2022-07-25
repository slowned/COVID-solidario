from flask import (
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session
)
from app.helpers.auth import authenticated
from app.helpers.auth import has_permission
from app.helpers import handler

from app.models.configuracion import Configuracion
from app.models.center import Turn

from . import turns

@turns.route('/turn/detail/<int:turn_id>', methods=['GET'])
def detail(turn_id):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_show'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    turn = Turn.query.filter_by(id=turn_id).first_or_404()
    return render_template('turns/detail.html', turn=turn, config=config)

@turns.route('/turn/list/', methods=['GET'], defaults={'page': 1})
@turns.route('/turn/list/<int:page>', methods=['GET'])
def list(page):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_show'):
        return handler.unauthorized_error(401)
    config = Configuracion.query.get(1)
    turns = Turn.query.filter_by()

    user_email = request.args.get('user_email')
    user_phone = request.args.get('user_phone')

    if user_email:
        search = "%{}%".format(user_email)
        turns = turns.filter(Turn.user_email.like(search))
    if user_phone:
        search = "%{}%".format(user_phone)
        turns = turns.filter(Turn.user_phone.like(search))

    turns = turns.paginate(page, int(config.elementos_cantidad), False)
    return render_template('turns/list.html', turns=turns, config=config)


@turns.route('/turn/delete/<int:turn_id>', methods=['GET', 'POST'])
def delete(turn_id):
    if not authenticated(session):
        flash("Debe estar logueado para acceder")
        return redirect(url_for("auths.login"))
    if not has_permission((session['current_user']['id']), 'user_destroy'):
        return handler.unauthorized_error(401)
    turn = Turn.query.filter_by(id=turn_id).first_or_404()
    turn.unassing_turn()
    return redirect(url_for('turns.list'))
