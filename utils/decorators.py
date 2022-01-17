import logging
from functools import wraps
from typing import Callable
from aiohttp import web
from authlib.jose.errors import DecodeError

from utils import jwt_token
from app.auth import storage as auth_storage


def with_user():
    def decorator(f: Callable):
        @wraps(f)
        async def decorated_f(req: web.Request, *args, **kwargs):
            token = req.headers["Authorization"].partition(' ')[2]

            try:
                login = (await jwt_token.decode(token)).get("login")
                user = await auth_storage.get_user(login)
            except DecodeError as e:
                logging.error(str(e))
                raise web.HTTPForbidden(text=f"Error on Authorization token decode")

            return await f(req, *args, **dict(kwargs, user=user))
        return decorated_f
    return decorator
