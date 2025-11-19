from sqlalchemy import Column, Integer, BigInteger, String, Text, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime

from ..database import Base


class ImgCaptcha(Base):
    __tablename__ = 'captcha'
    captchaId = Column(Integer, primary_key=True, autoincrement=True)
    captchaText = Column(String(4))
    genTime = Column(BigInteger)

    Captcha_expire = 5 * 60
    """验证码超时时间为300秒"""

    @staticmethod
    async def add(db: AsyncSession, captchaText: str):
        """添加新生成的验证码"""
        item = ImgCaptcha(captchaText=captchaText, genTime=int(datetime.now().timestamp()))
        db.add(item)
        await db.commit()

    @staticmethod
    async def check_captcha(db: AsyncSession, captchaText: str) -> bool:
        """检查验证码是否合法"""
        query = (select(func.count())
                 .where(ImgCaptcha.captchaText == captchaText,
                        ImgCaptcha.genTime >= datetime.now().timestamp() - ImgCaptcha.Captcha_expire)
                 .select_from(ImgCaptcha))
        result = await db.execute(query)
        count = result.scalar()
        return count > 0

    @staticmethod
    async def del_by_captchaText(db: AsyncSession, captchaText: str):
        """删除某验证码"""
        query=delete(ImgCaptcha).where(ImgCaptcha.captchaText == captchaText)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def del_all_expire(db: AsyncSession):
        """删除所有超时验证码"""
        query=delete(ImgCaptcha).where(ImgCaptcha.captchaText < datetime.now().timestamp()-ImgCaptcha.Captcha_expire)
        await db.execute(query)
        await db.commit()

