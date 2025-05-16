import json
import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import class_mapper

load_dotenv()
ADMINS = [905042750]
KITCHEN = [905042750]


def obj_to_dict(obj):
    return {column.name: getattr(obj, column.name)
            for column in class_mapper(obj.__class__).columns}


def result_to_json(result):
    result_list = [obj_to_dict(row) for row in result.fetchall()]
    return json.loads(json.dumps(result_list, ensure_ascii=False))


async def post_api(path: str, json):
    async with httpx.AsyncClient() as client:
        return (await client.post(f'http://127.0.0.1:8000/{path}', json=json,
                                  )).json()
