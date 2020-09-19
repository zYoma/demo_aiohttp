from aiohttp_session import get_session

from db import User


async def request_user_middleware(app, handler):
    async def middleware(request):
        request.session = await get_session(request)
        request.user = None
        user_id = request.session.get('user')
        if user_id is not None:
            request.user = await app.objects.get(User, id=user_id)

        return await handler(request)
    return middleware
