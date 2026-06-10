
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async_database_url = "mysql+aiomysql://root:123456@localhost/news_app?charset=utf8mb4"
# 创建数据库引擎
async_engine = create_async_engine(
    async_database_url, echo=True, pool_size=10, max_overflow=20)

# 创建会话工厂
async_session_local = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession)
async_session = async_session_local()

# 依赖项


async def get_db():
    async with async_session_local() as session:
        async with session.begin():  # begin事务，会自动commit
            yield session  # yield保持会话挂起，直到依赖项使用完毕
