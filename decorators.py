from functools import wraps
from flask import g, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('login', None):
            return redirect(url_for('adminlogin'))
        return f(*args, **kwargs)
    return decorated_function
