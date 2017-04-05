from config import PROJECT_ROOT
import aiohttp
import os


def public_page(x):
    return x


def authenticated_only(f):
    async def wrapped(request):
        if not request.app['current_user'].authenticated:
            raise aiohttp.web.HTTPFound('/login')
        else:
            return await f(request)
    return wrapped


def admin_only(f):
    @authenticated_only
    async def wrapped(request):
        if not request.app['current_user'].admin:
            raise aiohttp.web.HTTPForbidden()
        else:
            return await f(request)
    return wrapped


def pathfromroot(path):
    return os.path.join(PROJECT_ROOT, path)
