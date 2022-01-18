import logging
from typing import Callable

from aiohttp import web
from authlib.jose.errors import ExpiredTokenError, DecodeError

import conf
from app.router import public_routes, private_routes
from utils.auth import jwt_token
from utils.auth.jwt_token import extract_from_req


# Lifecycle
async def on_startup(_: web.Application):
    await conf.db.connect()


async def on_shutdown(_: web.Application):
    await conf.db.disconnect()


# Middlewares
@web.middleware
async def on_request(req: web.Request, handler: Callable):
    try:
        if req.match_info.route.resource.canonical in [pr.path for pr in public_routes]:
            return await handler(req)

        token = extract_from_req(req)
        await jwt_token.validate(token)
        return await handler(req)
    except ExpiredTokenError:
        raise web.HTTPForbidden(text="Token expired")
    except DecodeError as e:
        logging.error(str(e))
        raise web.HTTPForbidden(text="Error on Authorization token decode")


app = web.Application(middlewares=[on_request])

# Routes
app.add_routes([*public_routes, *private_routes])
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host="127.0.0.1", port=8080)
