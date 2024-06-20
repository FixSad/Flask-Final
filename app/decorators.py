from functools import wraps
from flask import redirect
from flask_login import current_user


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(role):
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
