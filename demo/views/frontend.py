from sqlalchemy import select
import aiohttp
from aiohttp_jinja2 import template
from .. import db


@template('index.html')
async def index(request):
    site_name = request.app['config'].get('site_name')
    return {'site_name': site_name}

async def post(request):
    async with request.app['db'].acquire() as conn:
        query = select([db.post])
        result = await conn.fetch(query)

    return aiohttp.web.Response(body=str(result))
