import json
import httpx
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
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


security = HTTPBearer()
api_token = os.getenv('TOKEN')


async def post_api(path: str, json):
    async with httpx.AsyncClient() as client:
        return (await client.post(f'http://127.0.0.1:8000/{path}', json=json,
                                  headers={"Authorization": f"Bearer {api_token}"})).json()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
