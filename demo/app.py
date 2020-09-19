import aioredis  # pip install aioredis
import jinja2
import aiohttp_jinja2  # pip install aiohttp-jinja2
import aiohttp_debugtoolbar  # pip install aiohttp_debugtoolbar
# import asyncpgsa  # pip install asyncpg asyncpgsa
import peewee_async  # pip install peewee-async aiopg

from aiohttp import web
from aiohttp_session import session_middleware  # pip install aiohttp-session
from aiohttp_session.redis_storage import RedisStorage

from .routes import setup_routes
from middlewares import request_user_middleware
import settings
from db import database


async def create_app(config: dict):
    """ Подключаем сесии, для хранения используем redis. """
    redis_pool = await aioredis.create_pool(settings.REDIS_CON)
    middlewares = [session_middleware(
        RedisStorage(redis_pool)), request_user_middleware]
    """ Подключаем debugtoolbar. """
    if settings.DEBUG:
        middlewares.append(aiohttp_debugtoolbar.middleware)

    app = web.Application(middlewares=middlewares)
    app.redis_pool = redis_pool
    app.wslist = {}  # для вебсокета
    app['config'] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('demo', 'templates')
    )
    if settings.DEBUG:
        aiohttp_debugtoolbar.setup(app, intercept_redirects=False)

    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    return app


async def on_start(app):
    config = app['config']
    # app['db'] = await asyncpgsa.create_pool(dsn=config['database_uri'])

    # db conn
    database.init(**settings.DATABASE)
    app.database = database
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database)

async def on_shutdown(app):
    await app.objects.close()  # Закрываем соедиение с БД
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
    await app.shutdown()
