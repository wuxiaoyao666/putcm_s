from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, BigInteger, String, Text, func, update, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import Base
from pydantic import BaseModel
from fastapi import Request


class User(Base):
    __tablename__ = 'userinfo'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)
    userRole = Column(Integer)
    recentlyView = Column(JSON)
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)
    lastLoginTime = Column(BigInteger)
    authToken = Column(String(100))

    @staticmethod
    async def login_check(db: AsyncSession, username: str, password: str) -> bool:
        """检查用户名和密码是否合法，合法则返回true，否则返回false"""
        query = select(func.count()).where(User.userName == username, User.password == password).select_from(User)
        result = await db.execute(query)
        count = result.scalar()
        return count > 0

    @staticmethod
    async def update_token(db: AsyncSession, username: str, password: str, token: str):
        query = update(User).where(User.userName == username, User.password == password).values({
            "lastLoginTime": datetime.now().timestamp(), "authToken": token
        })
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_bytoken(db: AsyncSession, token: str) -> User | None:
        query = select(User).where(User.authToken == token)
        res = await db.execute(query)
        return res.scalar_one_or_none()

    @staticmethod
    async def update_recentlyview(db: AsyncSession, userId:int,recentlyView:List[int]):
        query=update(User).where(User.userId == userId).values({"recentlyView":recentlyView})
        await db.execute(query)
        await db.commit()


class LoginReq(BaseModel):
    username: str
    password: str
    captcha: str


async def get_curr_user(request: Request) -> User:
    return getattr(request.state, 'user')
