from flask import Blueprint


auths = Blueprint('auths', __name__)
centers = Blueprint('centers', __name__)
configuraciones = Blueprint('configuraciones', __name__)
sitios_deshabilitados = Blueprint('sitios_deshabilitados', __name__)
users = Blueprint('users', __name__)
turns = Blueprint('turns', __name__)

from app.resources import auth
from app.resources import center
from app.resources import configuracion
from app.resources import sitio_deshabilitado
from app.resources import user
from app.resources import turn
