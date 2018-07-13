import asyncio
import time, uuid

from sqlalchemy import (
    MetaData, Table, Column, Integer,
    String, Date, Boolean, Text
    )
from aiomysql.sa import create_engine

__all__ = ['users', 'blogs', 'comments']

meta = MetaData()

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

users = Table(
    'users', meta,
    Column('id', String(50), primary_key=True, default=next_id),
    Column('email', String(50), nullable=False),
    Column('password', String(50), nullable=False),
    Column('name', String(50), nullable=False),
    Column('image', String(500), nullable=False),
    Column('created_at', Date, default=time.time, nullable=False),
    Column('admin', Boolean, nullable=False)
)

blogs = Table(
    'blogs', meta,
    Column('id', String(50), primary_key=True, default=next_id),
    Column('user_id', String(50), nullable=False),
    Column('user_name', String(50), nullable=False),
    Column('user_image', String(500), nullable=False),
    Column('name', String(50), nullable=False),
    Column('summary', String(200), nullable=False),
    Column('content', Text, nullable=False),
    Column('created_at', Date, default=time.time, nullable=False)
)

comments = Table(
    'comments', meta,
    Column('id', String(50), primary_key=True, default=next_id),
    Column('blog_id', String(50), nullable=False),
    Column('user_id', String(50), nullable=False),
    Column('user_name', String(50), nullable=False),
    Column('user_image', String(500), nullable=False),
    Column('content', Text, nullable=False),
    Column('created_at', Date, default=time.time, nullable=False)
)

@asyncio.coroutine
def init_db(app):
    conf = app['config']['mysql']
    print(conf)
    engine = yield from create_engine(
        db=conf['db'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
    )
    app['db'] = engine

@asyncio.coroutine
def close_db(app):
    app['db'].close()
    yield from app['db'].wait_closed()
