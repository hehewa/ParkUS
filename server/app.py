#! /usr/bin/env python

from aiohttp import web
import asyncio
from config import SECRET_KEY
import aiohttp_jinja2
import jinja2
from aiohttp_session import get_session
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from parkinglot import parkings
from user import User
from utils import authenticated_only, admin_only, public_page, pathfromroot
import db
import wshandler
import embeddedhandler


async def user_middleware(app, handler):
    async def middleware_handler(request):
        session = await get_session(request)
        user_id = session['user_id'] if 'user_id' in session else None
        request.app['current_user'] = User(user_id)
        return await handler(request)
    return middleware_handler


def jinja_view(name, wrapper=authenticated_only):
    async def view(request):
        return aiohttp_jinja2.render_template(
            name + '.html', request, {'user': request.app['current_user']}
        )
    return wrapper(view)


async def login_handler(request):
    session = await get_session(request)
    post = await request.post()
    if 'id' in post:
        session['user_id'] = int(post['id'])
        raise web.HTTPFound('/')
    return aiohttp_jinja2.render_template('login.html', request, {})


async def logout_handler(request):
    session = await get_session(request)
    if 'user_id' in session:
        del session['user_id']
    raise web.HTTPFound('/')


async def signup_handler(request):
    session = await get_session(request)
    post = await request.post()
    if 'email' in post:
        c = request.app['db'].execute(
            'insert into User ("E-Mail") values (?)', [post['email']]
        )
        request.app['db'].commit()
        session['user_id'] = int(c.lastrowid)
        raise web.HTTPFound('/')
    raise web.HTTPFound('/signup')

ws_to_mbed = asyncio.Queue()
mbed_to_ws = asyncio.Queue()
app = web.Application()
loop = asyncio.get_event_loop()

aiohttp_session.setup(app, EncryptedCookieStorage(SECRET_KEY))
app.middlewares.append(user_middleware)
db.setup(app)
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(pathfromroot('templates'))
)
wshandler.setup(app, ws_to_mbed, mbed_to_ws)
embeddedhandler.setup(app, ws_to_mbed, mbed_to_ws, loop)

app.router.add_get('/wsmap', wshandler.wshandler)
app.router.add_get('/', jinja_view("index"))
app.router.add_get('/login', jinja_view("login", wrapper=public_page))
app.router.add_post('/login', login_handler)
app.router.add_get('/signup', jinja_view("signup", wrapper=public_page))
app.router.add_post('/signup', signup_handler)
app.router.add_get('/stats', jinja_view("stats", wrapper=admin_only))
app.router.add_get('/account', jinja_view("account"))
app.router.add_get('/logout', logout_handler)
app.router.add_static('/static', pathfromroot('static'))

web.run_app(app, loop=loop)
