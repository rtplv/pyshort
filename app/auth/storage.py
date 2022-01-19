from typing import List

from pydantic import BaseModel

import conf
from datetime import datetime


class User(BaseModel):
    id: int
    login: str
    password: str
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    id: int
    token: str
    user_id: int
    created_at: datetime
    updated_at: datetime


async def create_user(login: str, password: str) -> int:
    query = "INSERT INTO users(login, password) " \
            "VALUES (:login, :password) RETURNING id"
    values = {
        "login": login,
        "password": password
    }

    return await conf.db.fetch_val(query, values)


async def get_user(login: str) -> User:
    query = "SELECT * FROM users where login = :login"
    values = {"login": login}

    user_map = await conf.db.fetch_one(query, values)
    return User.parse_obj(user_map) if user_map else None


async def create_token(token: str, user_id: int):
    query = "INSERT INTO tokens(token, user_id) " \
            "VALUES (:token, :user_id)"
    values = {
        "token": token,
        "user_id": user_id
    }

    await conf.db.execute(query, values)


async def get_tokens_by_user(user_id: int) -> List[Token]:
    query = "SELECT * FROM tokens " \
            "WHERE user_id = :user_id"

    sessions = await conf.db.fetch_all(query, {"user_id": user_id})
    return [Token.parse_obj(s) for s in sessions] if sessions else None
