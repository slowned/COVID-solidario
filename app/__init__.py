from os import path, environ
from flask import Flask, render_template, g, redirect, url_for
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy

from config import CONFIG




db = SQLAlchemy()


from app.resources import configuracion
from app.resources import sitio_deshabilitado
from app.helpers import sitio_habilitado
from app.models import Configuracion

# from app import db
from app.helpers import handler

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(CONFIG[env])

    # Configure db
    db.init_app(app)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)


    from app.helpers import auth as helper_auth
    # Funciones que se exportan al contexto de Jinja2
 
    app.jinja_options['extensions'].append('jinja2.ext.debug')
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_auth.has_permission)


    from app.resources import auths as auths_blueprint
    from app.resources.api import centers_api as centers_api_blueprint
    from app.resources import centers as centers_blueprint
    from app.resources import configuraciones as configuraciones_blueprint
    from app.resources import users as users_blueprint
    
    app.register_blueprint(auths_blueprint)
    app.register_blueprint(centers_api_blueprint)
    app.register_blueprint(centers_blueprint)
    app.register_blueprint(configuraciones_blueprint)
    app.register_blueprint(users_blueprint)


    from app.resources import sitios_deshabilitados as sitios_deshabilitados_blueprint
    app.register_blueprint(sitios_deshabilitados_blueprint)

    from app.resources import turns as turns_blueprint
    app.register_blueprint(turns_blueprint)

    # Ruta para el Home (usando decorator)

    @app.route("/")
    def home():
        config = Configuracion.all()
        if not(Configuracion.sitio_habilitado()):
            return redirect(url_for('sitios_deshabilitados.index'))
        else:
            return render_template("home.html", config=config)
    #     # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app
