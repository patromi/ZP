from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    '''Klasa odpowiedziana za baze danych w tabeli role'''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        '''funkcja pozwalajaca dodanie permisji danej roli'''
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        '''funkcja pozwalajaca zabranie permisji danej roli'''
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        '''przyrocenie permisji do stanu poczatkowego'''
        self.permissions = 0

    def has_permission(self, perm):
        '''sprawdzenie czy uzytkownik posiada permisje'''
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles(roles):
        """dodawnanie roli do bazy danych"""
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.reset_permissions()
        for perm in roles[r]:
            role.add_permission(perm)
        role.default = (role.name == default_role)
        db.session.add(role)
        db.session.commit()

    @staticmethod
    def better_insert_roles():
        roles = {
            'Admin': [Permission.LIKE, Permission.WRITE, Permission.MANAGER,
                      Permission.ADMIN]
        }
        Role.insert_roles(roles)
        roles = {
            'Manager': [Permission.LOOK,
                        Permission.WRITE, Permission.MANAGER]
        }
        Role.insert_roles(roles)
        roles = {
            'User': [Permission.LOOK, Permission.LIKE]}
        Role.insert_roles(roles)


class User(UserMixin, db.Model):
    """klasa odpowiedzialna za utworzenie tabeli user"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    subname = db.Column(db.String(64), index=True)
    numerphone = db.Column(db.String(64), index=True)
    nrrej = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        """automatyczne dodanie roli po zarejstrowaniu uzytkownika"""
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == 'patromi123@gmail.com':
                self.role = Role.query.filter_by(name='Admin').first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        """zabezpieczenie uniemozliwjace bezposrednie wywołanie hasza"""
        raise AttributeError('Nie można odczytać atrybutu password.')

    @password.setter
    def password(self, password):
        """wygenerowanie hasza hasła"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """sprawdzenie czy dany hasz = dobre hasło"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """wygenerowanie specjalnego tokena na 1h"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        '''potwierdzenie prawdilowego tokena'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        """sprawdzenie czy dany uzytkownik posiada dana permisje"""
        return self.role is not None and self.role.has_permission(perm
                                                                  )

    def is_administrator(self):
        """patrz wyzej admin"""
        return self.can(Permission.ADMIN)

    def is_Manager(self):
        """patrz wyzej manager"""
        return self.can(Permission.MANAGER)

    @staticmethod
    def verify_email(email):
        x = User.query.filter_by(email=email).first_or_404()
        if x is None:
            return True
        else:
            return False


class Permission:
    """Wszystkie dostepne permisje"""
    """LOOK =  Wyświetlanie parkingów
        LIKE = Polubienia parkingów
         MANAGER = Możliwość zarządzania swoimi parkingami
         ADMIN = Pełny dostęp wraz z narzędziami administracyjnymi"""
    LOOK = 1
    LIKE = 2
    WRITE = 4
    MANAGER = 8
    ADMIN = 16


class AnonymousUser(AnonymousUserMixin):
    """sprawdzenie permisji dla osob nie zarejstrowanych"""

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Parking(UserMixin, db.Model):
    '''tabela odpowiedzialna za tabele parking'''
    __tablename__ = 'parking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    adress = db.Column(db.String(64), index=True)
    number_of_parkings = db.Column(db.String(64), index=True)
    number_of_free_parkings = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(128), index=True)
    localisation = db.Column(db.String(64), index=True)

    @staticmethod
    def delete_parking(id):
        x = Parking.query.filter_by(id=id)
        if x is None:
            return False
        else:
            Parking.query.filter_by(id=id).delete()
            db.session.commit()
            return True

    @staticmethod
    def validate_user_id(id):
        x = User.query.filter_by(id=id).first_or_404()
        if not x.role_id == 3:
            return False
        try:
            if x is None:
                return False
            else:
                return True
        except:
            return None


class Parking_reservation(UserMixin, db.Model):
    '''tabela odpowiedzialna za tabele parking_reservation'''
    __tablename__ = 'parking_reservation'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    date_reservation = db.Column(db.Date, index=True)
    start_time_reservation = db.Column(db.Time, index=True)
    end_time_reservation = db.Column(db.Time, index=True)
    status = db.Column(db.Integer, index=True)

    @staticmethod
    def delete_reservation(id):
        x = Parking_reservation.query.filter_by(id=id)
        if x is None:
            return False
        else:
            Parking_reservation.query.filter_by(id=id).delete()
            db.session.commit()
            return True


class Parking_sensor_id(UserMixin, db.Model):
    '''tabela odpowiedzialna za id czujników'''
    __tablename__ = 'miejsce_sensor'
    sid = db.Column(db.BigInteger, primary_key=True)
    dist = db.Column(db.Integer, index=True)
    tim = db.Column(db.BigInteger, index=True)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))


class otwarcia_history(UserMixin, db.Model):
    """Tabela odpowiedzialna za otwieranie bramy"""
    __tablename__ = 'otwarcia_sensor'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start = db.Column(db.BigInteger, index=True)
    end = db.Column(db.BigInteger, index=True)


class Stats(UserMixin, db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    number_of_all_parkings = db.Column(db.Integer, primary_key=True, unique=True)
    number_of_all_parking_places = db.Column(db.Integer, primary_key=True, unique=True)
    number_of_cities_with_our_parking = db.Column(db.Integer, primary_key=True, unique=True)

    @staticmethod
    def cities():
        n_p = Parking.query.all()
        list = []
        lista_bez = []
        for i in n_p:
            list.append(i.adress)
        for i in list:
            if i not in lista_bez:
                lista_bez.append(i)
        return len(lista_bez)

    @staticmethod
    def places():
        places = Parking.query.all()
        a = 0
        for i in places:
            a += int(i.number_of_parkings)
        return a

    @staticmethod
    def stats():
        stats = Stats.query.filter_by(id=0).first()
        stats.number_of_all_parkings = Parking.query.count()
        stats.number_of_cities_with_our_parking = Stats.cities()
        stats.number_of_all_parking_places = Stats.places()
        db.session.add(stats)
        db.session.commit()

    @staticmethod
    def stats_setup():
        stats = Stats(id=0, number_of_all_parking_places=0, number_of_all_parkings=0,
                      number_of_cities_with_our_parking=0)
        db.session.add(stats)
        db.session.commit()
        Stats.stats()
