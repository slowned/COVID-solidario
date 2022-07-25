from datetime import datetime, timedelta, date
from app import db
from json import JSONEncoder
from sqlalchemy import UniqueConstraint, func, text
from sqlalchemy.exc import IntegrityError
from flask import jsonify

__all__ = ['Center', 'Center_type', 'Turn']


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%H:%M:%S")


def dump_date(value):
    if value is None:
        return None
    return value.strftime("%Y/%m/%d")


def parce_fecha(fecha):
    if isinstance(fecha, str):
        year = int(fecha[0:4])
        month = int(fecha[5:7])
        day = int(fecha[8:10])
        return date(year, month, day)
    else:
        return fecha


TURNS_MAPER = {
    '1': '9:00',
    '2': '9:30',
    '3': '10:00',
    '4': '10:30',
    '5': '11:00',
    '6': '11:30',
    '7': '12:00',
    '8': '12:30',
    '9': '13:00',
    '10': '13:30',
    '11': '14:00',
    '12': '14:30',
    '13': '15:00',
    '14': '15:30',
    '15': '16:00',
}


class Turn(db.Model):
    """
    """
    # TODO: unique together center_id, date, time
    __tablename__ = 'turns'
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('center_id', 'date', 'hora_inicio', name='uix_1'),
    )
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10))
    center_id = db.Column(
            db.Integer, db.ForeignKey('centers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_email = db.Column(db.String(100))
    user_phone = db.Column(db.String(50))
    hora_inicio = db.Column(db.String(100))
    hora_fin = db.Column(db.String(100))
    asignado = db.Column(db.Boolean)  # default false

    @classmethod
    def recurrent_turn_stats(cls):
        return db.session.query(
            Turn.numero,
            func.count(Turn.numero)
        ).group_by(
            Turn.numero
        ).filter(Turn.asignado==True).all()

    @classmethod
    def serialize_turn_stats(cls, turn):
        return {
            'hora_inicio': TURNS_MAPER.get(turn[0]),
            'hora_fin': TURNS_MAPER.get(str(int(turn[0]) + 1)),
            'turno_numero': turn[0],
            'cantidad': turn[1],
        }

    def _get_start(self):
        return TURNS_MAPER.get(self.numero)

    def _get_end(self):
        return TURNS_MAPER.get(str(int(self.numero) + 1))

    @property
    def serialize_turns(self):
        return {
            'pk': self.id,
            'centro_id': self.center_id,
            'hora_inicio': self._get_start(),
            'hora_fin': self._get_end(),
            'fecha': dump_date(self.date),
            "telefono_donante": self.user_phone,
        }

    @classmethod
    def filter_by_date(cls, date, center_id):
        return cls.query.filter_by(
            center_id=center_id,
            date=date
        )

    @classmethod
    def get_turns(cls, center_id, fecha, libres=False):
        """
        Retorna los turnos de un centro para los siguientes
        2 dias despues del dia seleccionado
        @params
            centro_id: Centro.id
            date: Date
        """

        start_date = parce_fecha(fecha)
        end_date = start_date + timedelta(days=2)

        qs = cls.query.filter(
            Turn.center_id==center_id,
            Turn.date>=start_date,
            Turn.date<=end_date,
        )
        if libres:
            qs = qs.filter(Turn.asignado==False)

        return qs

    def assing_user(self, form):
        self.asignado = True
        self.user_email = form.user_email.data
        self.user_phone = form.user_phone.data
        db.session.commit()
        return self

    def assing_user_api(self, form):
        self.asignado = True
        self.user_email = form.email_donante.data
        self.user_phone = form.telefono_donante.data
        db.session.commit()
        return self

    @classmethod
    def get_turn_by_datetime(cls, center_id, fecha, hora_inicio):
        fecha = parce_fecha(fecha)
        return Turn.query.filter(
            Turn.center_id==center_id,
            Turn.hora_inicio==hora_inicio,
            Turn.date==fecha,
            Turn.asignado==False,
        ).first()

    def unassing_turn(self):
        self.user_email = ''
        self.user_phone = ''
        self.asignado = False
        db.session.commit()
        return self



class Center(db.Model):

    __tablename__ = 'centers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    open_hour = db.Column(db.Time())
    close_hour = db.Column(db.Time())
    township = db.Column(db.String(60), default='La Plata')
    # Ver si requiere forzar la codificacion ascii
    web_site = db.Column(db.Text(2083), default='')
    email = db.Column(db.String(60), default='')
    status = db.Column(db.Boolean, default=True)
    view_protocol = db.Column(db.String(60), default='No disponible')
    #   Investigar
    #   https://geoalchemy-2.readthedocs.io/en/latest/
    lat = db.Column(db.String(40), default="-36.5315")
    lng = db.Column(db.String(40), default="-59.9221")
    publish = db.Column(db.String(20), default='Pendiente')
    center_type_id = db.Column(db.Integer, db.ForeignKey('center_type.id'), nullable=False)
    center_type = db.relationship('Center_type')
    turns = db.relationship('Turn', backref='center')

    def __repr__(self):
        return f'<center: {self.id}, {self.name}>'

    @classmethod
    def all(cls):
        return cls.query.all()

    @staticmethod
    def _daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def _create_turns(self):
        turns = []
        start_date = date.today()
        end_date = date(start_date.year, 12, 31)
        for single_date in self._daterange(start_date, end_date):
            for numero in TURNS_MAPER:
                try:
                    hora_fin = TURNS_MAPER[str(int(numero)+1)],
                except KeyError:
                    hora_fin = TURNS_MAPER[numero].replace('00', '30'),
                finally:
                    turn = Turn(
                        numero=numero,
                        center_id=self.id,
                        date=single_date,
                        user_email='',
                        user_phone='',
                        hora_inicio=TURNS_MAPER[numero],
                        hora_fin=hora_fin,
                        asignado=False,
                    )
                turns.append(turn)
        self.turns = turns

    @classmethod
    def create(cls, form):
        tipo_centro = form.center_type.raw_data
        tipo_centro = Center_type.query.filter(Center_type.id.in_(tipo_centro)).first()
        instance = cls(
            publish="Aceptado",
            name=form.name.data,
            address=form.address.data,
            phone=form.phone.data,
            open_hour=form.open_hour.data,
            close_hour=form.close_hour.data,
            center_type=tipo_centro,
            web_site=form.web_site.data,
            email=form.email.data,
            township=form.township.data,
            #status=form.name.status,
            #view_protocol=form.view_protocol.data,
            lat=form.lat.data,
            lng=form.lng.data,
            #publish=form.publish.data

        )
        instance._create_turns()
        db.session.add(instance)
        try:
            db.session.commit()
            created = True
        except:
            db.session.rollback()
            created = False
        return instance, created

    @classmethod
    def api_create(cls, form):

        """
        Duda sobre Parametro center_type:
        Si el parametro no esta definido                -> Valor por defecto en la BD
        Si el parametro esta definido y existe en BD    -> Fetch
        Si el parametro esta definido y no existe en BD -> Valor por defecto
                                                        -> o deberia salir con un 400 ?    
        """
        center_type_id = 0
        form_field = form["tipo"]
        if form_field.data:
            center_type = Center_type.find_by_name(form_field.data)
            if center_type:
                center_type_id = center_type.id
            else:
                return None, False

        instance = cls(
            name=form.nombre.data,
            address=form.direccion.data,
            phone=form.telefono.data,
            open_hour=form.hora_apertura.data,
            close_hour=form.hora_cierre.data,
            web_site=form.web.data,
            email=form.email.data,
            center_type_id=center_type_id,
            #Agregado para actividad 6
            lat=form.lat.data,
            lng=form.lng.data,
            township=form.municipio.data,
            #view_protocol=form.view_protocol.data,
        )
        instance._create_turns()
        db.session.add(instance)
        try:
            db.session.commit()
            created = True
        except:
            db.session.rollback()
            created = False
            instance = None
        return instance, created

    @classmethod
    def delete(cls, pk):
        center = Center.query.filter_by(id=pk).first_or_404()
        db.session.delete(center)
        db.session.commit()

    @classmethod
    def find_by_id(cls, center_id):
        return Center.query.filter(
            Center.id == center_id
        ).first()

    @classmethod
    def find_enabled_by_id(cls, center_id):
        return Center.query.filter(
            Center.id == center_id,
            Center.publish == "Aceptado",
            Center.status == True
        ).first()

    @classmethod
    def filter_enabled_all(cls):
        return Center.query.filter(
            Center.publish == "Aceptado",
            Center.status == True
        )

    @classmethod
    def centers_by_type(cls):
        def serializeStadistic(centro):
            return{
                'nombre': centro[0],
                'cantidad': centro[1]
            }
        #   session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
        #   return db.session.query(Center.center_type, func.count(Center.center_type)).group_by(Center.center_type).all()
        
        #return Center.query.all()
        #return db.session.query(Center.center_type, db.func.count(Center.center_type_id)).group_by(Center.center_type_id).all()
        centers= db.session.query(Center_type.name , db.func.count(Center_type.name).label("cantidad")).join(Center, Center_type.id == Center.center_type_id).group_by(Center_type.name).all()
        
        centers = [serializeStadistic(i) for i in centers] 

        return centers
        
    @classmethod
    def centers_by_township(cls):
        # Tambien podria traerlo desde la config
        QUERY_LIMIT = 5
        def serializeStadistic(result):
            return{
            'localidad': result[0],
            'cantidad_centros': result[1]
            }
        results= db.session.query(Center.township, func.count(Center.id).label('cantidad')).group_by(Center.township).order_by(text('cantidad DESC')).all()#.limit(5)
        #import ipdb;ipdb.set_trace()
        limit = len(results)
        limit = limit if limit<QUERY_LIMIT else QUERY_LIMIT
        stats = [serializeStadistic(results[i]) for i in range(limit)] 
        return stats

    #   
    #   Investigar
    #   https://flask-marshmallow.readthedocs.io/en/latest/
    #   https://marshmallow.readthedocs.io/en/stable/
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'pk': self.id,
            'lat': self.lat,
            'lng': self.lng,
            'nombre': self.name,
            'direccion': self.address,
            'telefono': self.phone,
            'hora_apertura': dump_datetime(self.open_hour),
            'hora_cierre': dump_datetime(self.close_hour),
            'tipo': self.center_type.name,
            'web': self.web_site,
            'email': self.email,
            'position': [self.lat, self.lng],
            }

    @classmethod
    def accept(cls, pk):
        center = Center.query.filter_by(id=pk).first_or_404()
        center.publish = 'Aceptado'
        db.session.commit()

    @classmethod
    def reject(cls, pk):
        center = Center.query.filter_by(id=pk).first_or_404()
        center.publish = 'Rechazado'
        db.session.commit()

    def update(self, form):
        tipo_centro = form.center_type.raw_data
        tipo_centro = Center_type.query.filter(Center_type.id.in_(tipo_centro)).first()
        self.name = form.name.data,
        self.address = form.address.data,
        self.phone = form.phone.data,
        self.open_hour = form.open_hour.data,
        self.close_hour = form.close_hour.data,
        self.township = form.township.data,
        #self.center_type = form.center_type.data,
        self.web_site = form.web_site.data,
        self.email = form.email.data,
            #status=form.name.status,
            #view_protocol=form.view_protocol.data,
        self.lat = form.lat.data,
        self.lng = form.lng.data
            #publish=form.publish.data
        db.session.commit()
        return self

    def get_turns_by_date(self, date):
        return self.query.filter(Turn.date == date).all()

    def get_available_turns(self, date):
        available_turns = TURNS_MAPER.copy()
        turns = self.query.filter(Turn.date == date).all()
        if turns:
            for t in turns:
                available_turns.pop(t.numero)
        return available_turns

    def serialize_available_turns(self, turns, date):
        serialized_turns = {"turnos": []}
        for turn in turns:
            aux_dict = {
                'pk': str(turn.id),
                'centro_id': str(turn.center_id),
                'hora_inicio': turn.hora_inicio,
                'hora_fin': turn.hora_fin,
                'fecha': dump_date(turn.date),
            }
            serialized_turns["turnos"].append(aux_dict)
        return serialized_turns

    @classmethod
    def set_view_protocol(cls, pk, file):
        center = Center.query.filter_by(id=pk).first_or_404()
        center.view_protocol = file
        db.session.commit()


class Center_type(db.Model):
    __tablename__ = 'center_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return Center_type.query.filter(
            Center_type.name == name
        ).first()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'nombre': self.name
        }

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
