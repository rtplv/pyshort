import math
import conf
from aiohttp import web
from datetime import datetime
from asyncpg import UniqueViolationError
from pydantic import BaseModel, ValidationError
from app.auth import storage
from app.auth.storage import User
from utils import jwt_token
from utils.decorators import with_user
from utils.json import json_response
from utils.password import validate_hash, generate_hash


class AuthCredentials(BaseModel):
    login: str
    password: str


async def login(req: web.Request) -> web.Response:
    try:
        body = await req.json()
        credentials = AuthCredentials(**body)
        user = await storage.get_user(credentials.login)

        if user is not None and validate_hash(credentials.password, user.password):
            token = await jwt_token.encode({
                "login": credentials.login,
                "exp": math.ceil(datetime.now().timestamp() + conf.JWT_EXPIRATION)
            })
            await storage.create_token(token, user.id)

            return json_response({"token": token})
        else:
            raise web.HTTPBadRequest(text="Invalid credentials")
    except ValidationError as e:
        raise web.HTTPBadRequest(text=f"login and password validation error: {str(e)}")


async def register(req: web.Request) -> web.Response:
    try:
        body = await req.json()
        credentials = AuthCredentials(**body)

        return json_response({
            "id": await storage.create_user(credentials.login, generate_hash(credentials.password))
        })
    except UniqueViolationError:
        raise web.HTTPBadRequest(text="user already exists")
    except ValidationError as e:
        raise web.HTTPBadRequest(text=f"login and password validation error: {str(e)}")


@with_user()
async def get_user(_: web.Request, user: User) -> web.Response:
    safe_user = user.__dict__.copy()
    del safe_user["password"]

    return json_response({
        "user": safe_user
    })
