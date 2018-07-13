
import logging
from aiohttp import web
import asyncio
from web.settings import get_config
from web.routes import setup_routes
import aiohttp_jinja2
import jinja2
from web.db import init_db, close_db

@asyncio.coroutine
def init_app(argv=None):
    app = web.Application()
    app['config'] = get_config(argv)

    aiohttp_jinja2.setup(app,
        loader=jinja2.PackageLoader('web', 'templates'))

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    setup_routes(app)

    return app

def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(argv)
    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
