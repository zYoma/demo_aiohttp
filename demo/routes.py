from .views import frontend, websocket
from settings import STATIC_DIR


def setup_routes(app):
    app.router.add_route('GET', '/', frontend.Index, name='index')
    app.router.add_route('GET', '/post', frontend.PostPage, name='post')
    app.router.add_route('GET', '/add-roles',
                         frontend.CreateRoles, name='create_roles')
    app.router.add_route(method='*', path='/login',
                         handler=frontend.LogIn, name='login')
    app.router.add_route(method='*', path='/reg',
                         handler=frontend.Registration, name='registration')
    app.router.add_route('GET', '/add', frontend.add_post, name='add_post')
    app.router.add_route('POST', '/add', frontend.add_post, name='add_post')
    app.router.add_route(
        'POST', r'/del/{id}', frontend.del_post, name='del_post')
    app.router.add_route(
        method='GET', path='/ws/{user}', handler=websocket.WebSocket, name='ws')

    app.router.add_static('/static', STATIC_DIR, name='static')
