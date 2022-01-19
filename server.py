import logging
from typing import Callable

import aiohttp_cors
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
        if req.method == "OPTIONS" or \
           req.match_info.route.resource.canonical in [pr.path for pr in public_routes]:
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
# Lifecycle events
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
# CORS
# WARN: only for dev
# cors = aiohttp_cors.setup(app, defaults={
#     "*": aiohttp_cors.ResourceOptions(
#         allow_credentials=True,
#         expose_headers="*",
#         allow_headers="*",
#         allow_methods="*"
#     )
# })

# for route in list(app.router.routes()):
#     cors.add(route)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(app)
