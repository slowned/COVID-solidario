from app import db

__all__ = ['Configuracion']


class Configuracion(db.Model):
    __tablename__ = 'configuraciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    elementos_cantidad = db.Column(db.String(60), nullable=False)
    mensaje_deshabilitado = db.Column(db.String(255), nullable=False)
    sitio_hab = db.Column(db.Boolean, default=True)

    @classmethod
    def all(cls):
        return Configuracion.query.get(1)

    @classmethod
    def modify(cls, nueva_config):

        config = Configuracion.query.get(1)
        config.titulo = nueva_config['titulo']
        config.descripcion = nueva_config['descripcion']
        config.email = nueva_config['email']
        config.elementos_cantidad = nueva_config['max_rows']
        config.mensaje_deshabilitado = nueva_config['mensaje_deshabilitado']
        if not ('sitio_habilitado') in nueva_config:
            nueva_config['sitio_habilitado'] = 0
            config.sitio_hab = 0
        else:
            config.sitio_hab = 1
            nueva_config['sitio_habilitado'] = 1
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def sitio_habilitado(cls):
        return Configuracion.query.get(1).sitio_hab

    @classmethod
    def items_paginas(cls):
        return Configuracion.query.get(1).elementos_cantidad

    @classmethod
    def msj_deshabilitado(cls):
        return Configuracion.query.get(1).mensaje_deshabilitado

