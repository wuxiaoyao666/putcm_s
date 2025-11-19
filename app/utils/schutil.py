from loguru import logger

from app.database import AsyncSessionLocal
from app.models.tmpfile import TmpFile

TmpFileExpireTime=60*60
"""临时上传文件超期时间，默认3600秒（1小时）"""
async def sch_clear_tmpfile():
    logger.info("开始执行定时清空超时图片任务")

    async with AsyncSessionLocal() as db:
        await TmpFile.expire_batch_del(db)
