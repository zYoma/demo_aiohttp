import hashlib

from aiohttp import web


def redirect(request, router_name, *, permanent=False, **kwargs):
    """ Redirect to given URL name """
    url = request.app.router[router_name].url_for(**kwargs)
    if permanent:
        raise web.HTTPMovedPermanently(url)
    raise web.HTTPFound(url)


def login_required(func):
    """ Allow only auth users """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            redirect(self.request, 'login')
        return await func(self, *args, **kwargs)
    return wrapped


def gen_hash(password: str):
    salt = 'sddg&*328923fdfl'
    str2hash = password + salt
    result = hashlib.md5(str2hash.encode())
    return result.hexdigest()
