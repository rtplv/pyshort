from aiohttp import web
from pydantic import BaseModel, ValidationError, HttpUrl

from app.auth.storage import User
from app.shortener import storage
from utils import base62
from utils.auth.decorators import with_user
from utils.response import json_response


class GenerateUrlRequest(BaseModel):
    original_url: HttpUrl
    user_id: int = None


async def generate_url(req: web.Request) -> web.Response:
    try:
        body = await req.json()
        gen_req = GenerateUrlRequest.parse_obj(body)

        url_id = await storage.create_url(
            gen_req.original_url,
            gen_req.user_id
        )

        return json_response({
            "short_id": base62.dehydrate(url_id)
        })
    except ValidationError as e:
        return json_response({
            "errors": e.errors()
        }, status=400)


async def resolve(req: web.Request) -> web.Response:
    short_id = req.match_info["short_id"]
    url = await storage.get_url_by_id(base62.saturate(short_id))
    return web.HTTPFound(url.original_url)


@with_user()
async def get_urls(_: web.Request, user: User) -> web.Response:
    urls = await storage.get_urls_by_user_id(user.id)
    urls_with_short = [{**u.__dict__, "short_id": base62.dehydrate(u.id)} for u in urls] if urls else []

    return json_response({
        "urls": urls_with_short
    })
