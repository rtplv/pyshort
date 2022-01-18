import functools
import ujson
from typing import List
from aiohttp import web

json_dumps = functools.partial(ujson.dumps, default=str)
json_response = functools.partial(web.json_response, dumps=json_dumps)


def json_error(errors: List[str], status: int = 400) -> web.Response:
    return json_response({
        "errors": errors
    }, status=status)
