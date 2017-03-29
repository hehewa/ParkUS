from flask import g, abort
from flask_login import current_user, login_required
from flask_socketio import disconnect
from config import DB_PATH
import sqlite3

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        def make_dicts(cursor, row):
             return dict((cursor.description[idx][0], value)
                        for idx, value in enumerate(row))
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def authenticated_only(f):
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

def admin_only(route):
    @login_required
    def wrapped():
        if current_user.admin:
            return route()
        else:
            abort(403)
    return wrapped
