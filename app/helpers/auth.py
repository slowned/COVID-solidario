from app.models.user import User
from app.models.configuracion import Configuracion


def authenticated(session):
    return session.get("current_user")


def session_update(session, user):
    session["current_user"] = {"id" : user.id,
                               "name": user.name,
                            }


def has_permission(user_id, permission):
	return User.has_permission(user_id, permission)


def find_by_email(user_input):
	return User.filter_one_by_email_and_username(
        email=user_input,
        user_name=user_input,
        )


def site_down():
    return not Configuracion.sitio_habilitado()


def current_user(user_id):
	return User.find_by_id(user_id)


def is_not_active(user):
	return user.is_active() == False


def is_not_admin(user):
	return user.has_role('ROL_ADMINISTRADOR') == False
