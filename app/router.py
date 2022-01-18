from aiohttp import web
from app.auth.handlers import get_user, login, register
from app.shortener.handlers import generate_url, get_urls, resolve

v1_prefix = "/api/v1"

public_routes = [
    web.get("/{short_id}", resolve),
    web.post(f"{v1_prefix}/shortener/generate", generate_url),
    web.post(f"{v1_prefix}/auth/register", register),
    web.post(f"{v1_prefix}/auth/login", login),
]

private_routes = [
    web.get(f"{v1_prefix}/auth/user", get_user),
    web.get(f"{v1_prefix}/shortener/urls", get_urls)
]
