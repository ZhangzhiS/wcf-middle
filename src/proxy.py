import os

import aiofiles
import httpx
from fastapi import APIRouter, Body
from fastapi.requests import Request
from pydantic import BaseModel

proxy_router = APIRouter()


class ProxyImageData(BaseModel):
    path: str
    receiver: str


@proxy_router.post("/proxy/image")
async def proxy_image(requests: Request, data: ProxyImageData = Body(...)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=data.path,
        )
    if response.status_code != 200:
        return {"success": False}
    filename = os.path.basename(data.path)
    file_path = os.path.expanduser("~")
    w_path = os.path.join(file_path, filename)
    async with aiofiles.open(w_path, "wb") as f:
        # async with aiofiles.open(filename, "wb") as f:
        await f.write(response.content)
    wcf_url = str(requests.base_url)
    print(wcf_url)
    print(requests.url.path)
    # data.path = w_path
    # async with httpx.AsyncClient() as client:
    #     return client.post(wcf_url, json=data.model_dump())
