import logging

import aiohttp
from aiohttp import web

import conf
from app.router import routes


async def on_startup(app: web.Application):
    await conf.db.connect()


async def on_shutdown(app: web.Application):
    await conf.db.disconnect()


app = web.Application()

app.add_routes(routes)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app)
