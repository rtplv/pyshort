import logging
from functools import wraps
from typing import Callable
from aiohttp import web
from authlib.jose.errors import DecodeError, ExpiredTokenError

from utils.auth import jwt_token
from app.auth import storage as auth_storage
from utils.auth.jwt_token import extract_from_req


def with_user():
    def decorator(f: Callable):
        @wraps(f)
        async def decorated_f(req: web.Request):
            token = extract_from_req(req)

            try:
                login = (await jwt_token.decode(token)).get("login")
                user = await auth_storage.get_user(login)

                req["user"] = user
                return await f(req, user)
            except ExpiredTokenError:
                raise web.HTTPForbidden(text="Token expired")
            except DecodeError as e:
                logging.error(str(e))
                raise web.HTTPForbidden(text="Error on Authorization token decode")
        return decorated_f
    return decorator
