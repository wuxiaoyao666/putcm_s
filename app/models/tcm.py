from datetime import datetime
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import Column, Integer, BigInteger, String, Text, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path
from aiofiles import os
from pypinyin import pinyin, Style
import aiofiles.os as async_os
import shutil

from .tmpfile import TmpFile
from .user import User
from ..database import Base


class Tcm(Base):
    __tablename__ = "tcm"
    tcmId = Column(Integer, primary_key=True, autoincrement=True)
    tcmName = Column(String(100), unique=True, nullable=False, comment="中药名")
    letterIndex = Column(String(1), comment="首字母索引")
    allLetter = Column(String(255), comment="全拼，用于同字母排序")
    tcmImg = Column(String(100), comment="图片完整路径，从/tcm开始，含后缀")
    insertUserId = Column(Integer, comment="用户ID，关联表userinfo")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, item: TcmReq, insertUserId: int = 0):
        """提前上传图片文件，保存到临时文件"""
        localPath = item.tcmImg[len("/api/"):]
        if not await os.path.isfile(localPath):
            raise FileNotFoundError(f"文件 {item.tcmImg} 不存在")
        now = int(datetime.now().timestamp())
        # 得到最大tcmId
        max_query = select(func.max(Tcm.tcmId)).select_from(Tcm)
        max_res = await db.execute(max_query)
        max = max_res.scalar_one_or_none()
        if max:
            max = max + 1
        else:
            max = 1
        # 得到首字母
        pinyin_list = pinyin(item.tcmName, style=Style.NORMAL, heteronym=False)
        allLetter = ''.join([item[0] for item in pinyin_list])
        letterIndex = allLetter[0].upper()  # 得到首字母，并转为大写
        item = Tcm(tcmId=max, tcmName=item.tcmName, letterIndex=letterIndex, allLetter=allLetter, tcmImg=item.tcmImg,
                   insertUserId=insertUserId, insertTime=now, updateTime=now)
        db.add(item)
        await db.commit()
        await TmpFile.delRecord(db, item.tcmImg)  # 删除临时文件记录，避免超时文件被清掉

    @staticmethod
    async def get_list(db: AsyncSession, page: int, perPage: int):

        # 计算偏移量
        offset = (page - 1) * perPage
        # 计算总数
        total_query = select(func.count()).select_from(Tcm)
        total_res = await db.execute(total_query)
        total = total_res.scalar()
        # 查询分页数据
        items_query = (select(Tcm.tcmId, Tcm.tcmName, Tcm.tcmImg, Tcm.insertTime, User.userName.label("insertUser"))
                       .select_from(Tcm)
                       .outerjoin(User, Tcm.insertUserId == User.userId)
                       .offset(offset)
                       .limit(perPage))
        items_res = await db.execute(items_query)
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def del_by_tcmId(db: AsyncSession, tcmId: int):
        # todo:删除数据表(15张）
        # 删除文件目录
        local_path = f"file/{tcmId}"
        if os.path.exists(local_path):
            shutil.rmtree(local_path, ignore_errors=True)
        # 读中药图片
        query = select(Tcm.tcmImg).where(Tcm.tcmId == tcmId)
        res = await db.execute(query)
        tcmImg = res.scalar_one_or_none()
        # 删中药图片
        if tcmImg:
            localPath = tcmImg[len("/api/"):]
            if Path(localPath).exists():
                await async_os.remove(localPath)
        # 删中药表1行
        del_query = delete(Tcm).where(Tcm.tcmId == tcmId)
        await db.execute(del_query)
        await db.commit()

    @staticmethod
    async def get_by_tcmIds(db: AsyncSession, tcmIds: List[int]):
        query = select(Tcm.tcmId, Tcm.tcmName, Tcm.tcmImg).where(Tcm.tcmId.in_(tcmIds))
        res = await db.execute(query)
        return res.mappings().all()

    # @staticmethod
    # async def get_all(db: AsyncSession):
    #     query = select(Tcm.tcmId, Tcm.tcmName, Tcm.tcmImg, Tcm.letterIndex)
    #     res = await db.execute(query)
    #     return res.mappings().all()

    @staticmethod
    async def get_letters(db: AsyncSession):
        query = select(Tcm.letterIndex).distinct()
        res = await db.execute(query)
        return res.scalars().all()

    @staticmethod
    def group_by_letter_index(original_list: list):
        # 用于临时存储分组结果的字典，键为letterIndex的值，值为对应组的items列表
        groups = {}

        for item in original_list:
            # 获取当前item的letterIndex（假设所有元素都包含该字段）
            key = item.get('letterIndex')
            if key is None:
                continue  # 跳过不包含letterIndex字段的元素

            # 如果该key不存在于groups中，则初始化一个空列表
            if key not in groups:
                groups[key] = []

            # 将当前item添加到对应分组的列表中
            groups[key].append(item)

        # 转换为目标格式的列表：[{"letterIndex": key, "items": items}, ...]
        result = [{"letterIndex": key, "items": items} for key, items in groups.items()]

        return result

    @staticmethod
    async def get_by_letter(db: AsyncSession, letter: str):
        query = select(Tcm.tcmId, Tcm.tcmName, Tcm.tcmImg).where(Tcm.letterIndex == letter).order_by(Tcm.allLetter)
        res = await db.execute(query)
        return res.mappings().all()

    @staticmethod
    async def get_tcmName(db:AsyncSession,tcmId:int):
        query=select(Tcm.tcmName).where(Tcm.tcmId == tcmId)
        res=await db.execute(query)
        return res.scalar()


class TcmReq(BaseModel):
    tcmName: str
    tcmImg: str
