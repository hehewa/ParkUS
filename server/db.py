from config import DB_PATH
import sqlite3

db = None


def get_db():
    global db
    if db is not None:
        return db
    else:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = make_dicts
        return db


def make_dicts(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}


async def db_shutdown(app):
    app['db'].close()


def setup(app):
    global db
    app['db'] = db = sqlite3.connect(DB_PATH)
    app['db'].row_factory = make_dicts
    app.on_shutdown.append(db_shutdown)
