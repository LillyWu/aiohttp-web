import aiohttp_jinja2

from . import db

@aiohttp_jinja2.template('blogs.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.blogs.select())
        records = await cursor.fetchall()
        blogs = [dict(q) for q in records]
        return {'blogs': blogs}
