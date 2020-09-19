import aiohttp
import peewee
from aiohttp_jinja2 import template

from ..db import Post, Role, User
from .. utils import login_required, gen_hash, redirect


class Index(aiohttp.web.View):

    #@login_required
    @template('index.html')
    async def get(self):
        ip = self.request.remote
        return {'ip': ip}


@template('add.html')
async def add_post(request):
    if request.method == 'POST':
        app = request.app
        data = await request.post()
        title = data['title']
        body = data['text']
        await app.objects.create(Post, title=title, body=body)

        raise aiohttp.web.HTTPFound('post')
    return {}


async def del_post(request):
    if request.method == 'POST':
        app = request.app
        post_id = request.match_info['id']
        post = await app.objects.get(Post, id=post_id)
        await app.objects.delete(post)

        raise aiohttp.web.HTTPFound('/post')


class PostPage(aiohttp.web.View):

    @template('post.html')
    async def get(self):
        app = self.request.app
        # result = await Post.all_posts(self.request.app.objects)
        result = await app.objects.execute(Post.select())

        return {'result': result}


class LogIn(aiohttp.web.View):

    @template('login.html')
    async def get(self):
        return {}

    async def post(self):
        """ Проверяем email """
        user = await self.is_valid()
        if not user:
            redirect(self.request, 'login')

        await self.login_user(user)

    async def login_user(self, user):
        """ Заносим id пользователя в сессию """
        self.request.session['user'] = str(user.id)
        redirect(self.request, 'post')

    async def is_valid(self):
        """ Проверяем пользователя и пароль """
        app = self.request.app
        data = await self.request.post()
        email = data.get('email', '')
        password = data.get('password', '')
        pass_hash = gen_hash(password)
        try:
            user = await app.objects.get(User, email=email, password=pass_hash)
        except peewee.DoesNotExist:
            return False

        return user


class Registration(aiohttp.web.View):

    @template('reg.html')
    async def get(self):
        return {}

    async def post(self):
        """ Делаем валидацию """
        user = await self.is_valid()
        if not user:
            redirect(self.request, 'registration')

        await self.create_user(user)

    async def create_user(self, data):
        """ Создаем пользователя. """
        app = self.request.app
        email = data.get('email', '')
        password = data.get('password1', '')
        pass_hash = gen_hash(password)
        role = await app.objects.get(Role, name='user')
        new_user = await app.objects.create(User, email=email, password=pass_hash, role=role)

        redirect(self.request, 'login')

    async def is_valid(self):
        """ Валидируем данные """
        app = self.request.app
        data = await self.request.post()
        email = data.get('email', '')
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        if password1 != password2:
            return False
        try:
            user = await app.objects.get(User, email=email)
        except peewee.DoesNotExist:
            return data
        else:
            return False


class CreateRoles(aiohttp.web.View):

    async def get(self):
        app = self.request.app
        roles = [('admin', 'Админ'), ('user', 'Пользователь')]
        for role in roles:
            await app.objects.create_or_get(Role, name=role[0], description=role[1])
        redirect(self.request, 'post')
