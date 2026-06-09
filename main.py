from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy import DateTime, Float, Integer, String, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.responses import PlainTextResponse
from routers.news import router
from pydantic import BaseModel, Field

app = FastAPI()
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
