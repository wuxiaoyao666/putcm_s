from datetime import datetime

import aiofiles
import aiofiles.os as async_os
from fastapi import UploadFile
from loguru import logger
from sqlalchemy import Column, Integer, String, BigInteger, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from pathlib import Path

from app.database import Base
from app.extensions import snowflake


class TmpFile(Base):
    __tablename__ = "tmpfile"
    tmpFileId = Column(Integer, primary_key=True, autoincrement=True)
    tmpFilePath = Column(String(100), comment="如：/api/file/父路径/文件，实际找文件时，去掉/api，找本地/file开头文件")
    fileDesc = Column(String(100))
    insertTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, file: UploadFile, parent_path: str, file_desc: str) -> str | None:
        """添加路径到临时文件
        Args:
            file:web上传的文件，含文件名和文件内容
            parent_path:父路径，如：/tcm,/1/bencao
            file_desc:文件描述
        Returns:
            新文件名，含扩展名
        """
        # 1.生成正式文件
        ext = Path(file.filename).suffix
        filename = f"{next(snowflake)}{ext}"
        localFilePath = f"{parent_path}/{filename}"
        tmpFilePath = f"/api/file{localFilePath}"
        # 2.数据库添加1行
        insertTime = int(datetime.now().timestamp())
        item = TmpFile(tmpFilePath=tmpFilePath, fileDesc=file_desc, insertTime=insertTime)
        db.add(item)
        await db.commit()
        # 3.保存文件
        try:
            local_parent=f"file/{parent_path}"
            Path(local_parent).mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(f"file{localFilePath}", mode="wb") as f:
                while content := await file.read(1024 * 1024):
                    await f.write(content)
        except Exception as e:
            logger.info(e)
        finally:
            await file.close()
        return tmpFilePath

    @staticmethod
    async def query(db: AsyncSession, allPath: str) -> bool:
        """查询文件记录是否存在数据库"""
        query = select(func.count()).where(TmpFile.tmpFilePath == allPath).select_from(TmpFile)
        result = await db.execute(query)
        count = result.scalar()
        return count > 0

    @staticmethod
    async def delRecord(db: AsyncSession, allPath: str):
        """删除记录，不删除文件。用于正常添加、编辑成功的场景"""
        query = delete(TmpFile).where(TmpFile.tmpFilePath == allPath)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def expire_batch_del(db: AsyncSession):
        """批量删除超期记录和文件"""
        # 1.查询超期文件
        now = int(datetime.now().timestamp())
        from app.utils.schutil import TmpFileExpireTime
        expireLastTime = now - TmpFileExpireTime
        query = select(TmpFile.tmpFilePath).where(TmpFile.insertTime < expireLastTime)
        res = await db.execute(query)
        rows = res.scalars().all()  # 返回多个对象，因查询的单个字段，所以返回的是字符串数组

        # 2.删除磁盘路径文件
        for row in rows:
            localPath = row[len("/api/"):]
            if Path(localPath).exists():
                await async_os.remove(localPath)

        # 3.批量删除记录
        if len(rows) > 0:
            query = delete(TmpFile).where(TmpFile.insertTime < expireLastTime)
            await db.execute(query)
            await db.commit()
            logger.info(f"清空超期失效文件{len(rows)}个")
        else:
            logger.info("超期文件数为0")
