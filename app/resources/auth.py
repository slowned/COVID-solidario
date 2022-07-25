from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from app.helpers.auth import authenticated, session_update, find_by_email, site_down, is_not_active, is_not_admin

from app.forms.login import CreateLoginForm
from . import auths
from app.models.configuracion import Configuracion

@auths.route('/login', methods=['GET', 'POST'])
def login():
    if authenticated(session):
        return redirect(url_for("home"))

    form = CreateLoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = find_by_email(form.email.data)
            if not user or user.verify_password(form.password.data) == False :
                flash("Usuario o clave incorrecto.")
                return redirect(url_for("auths.login"))
            if is_not_admin(user):
                if is_not_active(user):
                    flash("Tu cuenta de usuario ha sido deshabilitada")
                    return redirect(url_for("auths.login"))

                if site_down():
                    return redirect(url_for("sitios_deshabilitados.index"))

            session_update(session,user)

            return redirect(url_for("home"))
    config = Configuracion.query.get(1)
    return render_template("auth/login.html", form=form , config=config)


@auths.route('/logout')
def logout():
    try:
        del session["current_user"]
    except (KeyError):
        #La sesión ya estaba mortadela parece
        pass
    finally:
        session.clear()
    return redirect(url_for("auths.login"))
