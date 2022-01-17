from aiohttp import web
from app.auth.handlers import get_user, login, register


routes = [
    # Auth
    web.post("/api/v1/auth/register", register),
    web.post("/api/v1/auth/login", login),
    web.get("/api/v1/auth/user", get_user),
]
