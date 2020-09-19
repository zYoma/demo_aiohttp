# pip install peewee-async aiopg
import peewee
import peewee_async
from datetime import datetime
import peeweedbevolve  # pip install peewee-db-evolve

import settings


database = peewee_async.PostgresqlDatabase(None)


class BaseModel(peewee.Model):

    class Meta:
        database = database


class Post(BaseModel):
    title = peewee.CharField(max_length=50, verbose_name='Заголовок')
    body = peewee.TextField(verbose_name='Текст поста')
    created_at = peewee.DateTimeField(default=datetime.now)

    @classmethod
    async def all_posts(cls, objects):
        return await objects.execute(cls.select())

    def __str__(self):
        return self.title

    class Meta:
        order_by = ('created_at', )


class Role(BaseModel):
    name = peewee.CharField(max_length=50, unique=True, verbose_name='Имя')
    description = peewee.CharField(max_length=100, verbose_name='Описание')

    def __str__(self):
        return self.name


class User(BaseModel):
    email = peewee.CharField(max_length=50, verbose_name='Почта')
    password = peewee.CharField(max_length=100, verbose_name='Пароль')
    active = peewee.BooleanField(default=True, verbose_name='Статус')
    #roles = peewee.ManyToManyField(Role, backref='users')
    role = peewee.ForeignKeyField(Role, null=True, related_name='users')

    def __str__(self):
        return self.email


if __name__ == '__main__':
    database.init(**settings.DATABASE)
    database.evolve()
