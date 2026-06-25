from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from routers import favourite, news, users
from utils.exception_handler import exception_handler

app = FastAPI()
# 异常处理函数
exception_handler(app)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favourite.router)
# 配置CORS，解决跨域问题
origin = ["http://localhost:5173"]
app.add_middleware(

    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    