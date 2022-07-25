from sqlalchemy import or_ 
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

__all__ = ['User', 'Permission', 'Role']

user_has_role = db.Table('user_has_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))
    user_name = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    # Define the relationship to Role via UserRoles
    # roles = db.relationship('Rol', secondary='user_roles')
    role = db.relationship("Role", secondary=user_has_role)

    def __repr__(self):
        return f'<User: {self.id}, {self.user_name}>'

    @classmethod
    def find_by_id(cls, user_id):
        return User.query.filter(
            User.id == user_id
        ).first()

    @classmethod
    def has_permission(cls, user_id, permission):
        result = User.query.filter(User.id == user_id).join(User.role).join(Role.permissions).filter(Permission.name == permission).first()
        return True if result else False

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, form):
        roles = form.roles.raw_data
        roles = Role.query.filter(Role.name.in_(roles)).all()
        instance = cls(
            name=form.name.data,
            surname=form.surname.data,
            user_name=form.user_name.data,
            email=form.email.data,
            password=form.password.data,
            role=roles,
        )
        db.session.add(instance)
        try:
            db.session.commit()
            created = True
        except:
            db.session.rollback()
            created = False
        return instance, created

    @classmethod
    def delete(cls, pk):
        user = User.query.filter_by(id=pk).first_or_404()
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def find_by_email_and_pass(cls, email, password):
        return User.query.filter(or_(
            User.email == email,
            User.password == password,
        )).all()

    @classmethod
    def filter_by_email_and_username(cls, email, user_name):
        return cls.query.filter(or_(
            User.email == email,
            User.user_name == user_name
        )).all()

    @classmethod
    def filter_one_by_email_and_username(cls, email, user_name):
        return cls.query.filter(or_(
            User.email == email,
            User.user_name == user_name
        )).first()

    @classmethod
    def filter_by_username(cls, username):
        return cls.query.filter(or_(
            User.user_name.like(username)
        )).all()

    @property
    def password(self):
        """
        Impide que se pueda leer la clave de usuario
        """
        raise AttributeError('password: no es un atributo de lectura. :D')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update(self, form):
        self.name = form.name.data
        self.surname = form.surname.data
        self.user_name = form.user_name.data
        self.email = form.email.data
        self.active = form.active.data
        db.session.commit()
        return self

    def is_active(self):
        return self.active == True

    def has_role(self, role_name):
        role = Role.find_by_name(role_name)
        return role in self.role


role_has_permission = db.Table('role_has_permission', db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)


class Role(db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    permissions = db.relationship("Permission", secondary=role_has_permission)

    def __repr__(self):
        return self.name

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return Role.query.filter(
            Role.name == name
        ).first()


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return Permission.query.filter(
            Permission.name == name
        ).first()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
