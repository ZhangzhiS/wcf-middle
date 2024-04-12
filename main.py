#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
from typing import List
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.proxy import proxy_router

ALLOWED_HOSTS: List[str] = ["http://localhost:3002"]
ALLOWED_METHODS: List[str] = ["*"]
ALLOWED_HEADERS: List[str] = ["*"]


def create_app() -> FastAPI:
    fast_app = FastAPI(title="middle-service")
    register_middleware(fast_app)
    register_route(fast_app)
    return fast_app


def register_middleware(fast_app):
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=ALLOWED_METHODS,
        allow_headers=ALLOWED_HEADERS,
    )


def register_route(fast_app):
    fast_app.include_router(proxy_router)


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088, debug=True)
