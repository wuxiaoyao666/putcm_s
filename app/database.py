from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URI = "mysql+aiomysql://root:Mlz1210.@47.93.2.246:3306/putcm"
SQLALCHEMY_ECHO = True  # 打印SQL日志（调试）

# 异步引擎
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=SQLALCHEMY_ECHO)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession,autocommit=False, autoflush=False, expire_on_commit=False)

# 模型基类（与同步模式相同）
Base = declarative_base()


# 异步依赖项：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()  # 异步关闭会话
