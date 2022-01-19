import functools
import ujson
from aiohttp import web

json_dumps = functools.partial(ujson.dumps, default=str)
json_response = functools.partial(web.json_response, dumps=json_dumps)
