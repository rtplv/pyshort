from datetime import datetime
from pydantic import BaseModel

import conf


class Url(BaseModel):
    id: int
    original_url: str
    user_id: int
    created_at: datetime
    updated_at: datetime


async def create_url(original_url: str, user_id: int = None) -> int:
    query = "INSERT INTO urls(original_url, user_id)" \
            "VALUES (:original_url, :user_id) RETURNING id"
    values = {
        "original_url": original_url,
        "user_id": user_id
    }

    return await conf.db.fetch_val(query, values)


async def get_url_by_id(id: int) -> Url:
    query = "SELECT * FROM urls WHERE id = :id"
    values = {
        "id": id
    }

    url = await conf.db.fetch_one(query, values)

    return Url.parse_obj(url) if url else None


async def get_urls_by_user_id(user_id: int):
    query = "SELECT * FROM urls WHERE user_id = :user_id"
    values = {"user_id": user_id}

    urls = await conf.db.fetch_all(query, values)

    return [Url.parse_obj(u) for u in urls] if urls else None

