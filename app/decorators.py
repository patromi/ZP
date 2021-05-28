from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    '''decodator sprawdzajacy czy dany użytkownik posiada odpowiednia permisje'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(404)
                return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return decorated_function

    return decorator


def admin_required(f):
    '''tutaj dla admin'''
    return permission_required(Permission.ADMIN)(f)

def manager_required(f):
    '''tutaj dla zarzadcy'''
    return permission_required(Permission.MANAGER)(f)
