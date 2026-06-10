from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.responses import PlainTextResponse
from routers.news import router
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(router)

# 配置CORS，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
