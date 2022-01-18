import os
import sys
from asyncio.log import logger
from typing import Dict, Any

import aiofiles
from aiohttp import web
from authlib.jose import jwt, JWTClaims
from conf import ROOT_PATH


async def encode(payload: Dict[str, Any]) -> str:
    header = {"alg": "RS256"}
    private_key = await __load_key("rs256.key")
    return jwt.encode(header=header, payload=payload, key=private_key).decode()


async def decode(token: str) -> JWTClaims:
    public_key = await __load_key("rs256.key.pub")
    claims = jwt.decode(bytes(token, encoding="utf8"), public_key)
    return claims


async def validate(token: str) -> None:
    claims = await decode(token)
    claims.validate()


def extract_from_req(req: web.Request):
    return req.headers["Authorization"].partition(' ')[2]


async def __load_key(file_name: str) -> str:
    try:
        async with aiofiles.open(os.path.join(ROOT_PATH, "keys", f"{file_name}"), "r") as key_file:
            return (await key_file.read()).rstrip()
    except FileNotFoundError as e:
        logger.error("Token is not generated", e)
        sys.exit(1)
