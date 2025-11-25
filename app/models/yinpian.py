import io
from datetime import datetime

from aiofiles import os
from sqlalchemy import Column, Integer, TEXT, JSON, BigInteger, func, insert, update, Select, delete
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import tempfile
from pathlib import Path
import aiofiles.os as async_os

from .tcm import Tcm
from .tmpfile import TmpFile
from ..database import Base
from ..utils.imgutil import ImageTitle
from ..utils.listutil import ListContentLen, sql_build_start
from .user import User

class Yinpian(Base):
    __tablename__ = "yinpian"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材基源")
    t2 = Column(TEXT, comment="药材产地")
    t3 = Column(TEXT, comment="炮制沿革")
    t4 = Column(TEXT, comment="炮制品种")
    t5 = Column(TEXT, comment="炮制工艺")
    t6 = Column(TEXT, comment="饮片性状")
    t7 = Column(TEXT, comment="成分变化")
    t8 = Column(TEXT, comment="炮制作用")
    t9 = Column(TEXT, comment="临床应用")
    t10 = Column(TEXT, comment="处方应付")
    t11 = Column(TEXT, comment="贮藏条件")
    t12 = Column(TEXT, comment="质量标准")
    i1 = Column(JSON, comment="生品图片（list，{img,title}")
    i2 = Column(JSON, comment="制品图片（list，{img,title}")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: YinpianReq, userId: int):
        # 检查图片是否存在
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                localPath = sub.img[len("/api/"):]
                if not await os.path.isfile(localPath):
                    raise FileNotFoundError(f"{sub.title} 图片不存在")
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Yinpian).values(**values)
        await db.execute(query)
        await db.commit()
        # 删除临时文件记录
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                await TmpFile.delRecord(db, sub.img)

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: YinpianQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Yinpian.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Yinpian, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Yinpian.subId,
                             sql_build_start(Yinpian.t1, "st1"),
                             sql_build_start(Yinpian.t2, "st2"),
                             sql_build_start(Yinpian.t4, "st4"),
                             sql_build_start(Yinpian.t5, "st5"),
                             sql_build_start(Yinpian.t6, "st6"),
                             sql_build_start(Yinpian.t7, "st7"),
                             sql_build_start(Yinpian.t8, "st8"),
                             User.userName.label("updateUser"),
                             Yinpian.updateTime
                             ).outerjoin(User, Yinpian.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Yinpian.t1, Yinpian.t2, Yinpian.t3, Yinpian.t4, Yinpian.t5, Yinpian.t6, Yinpian.t7, Yinpian.t8, Yinpian.t9, Yinpian.t10, Yinpian.t11,
                   Yinpian.t12,
                   func.JSON_LENGTH(Yinpian.i1).label("si1"),
                   func.JSON_LENGTH(Yinpian.i2).label("si2"),
                   User.userName.label("updateUser"), Yinpian.updateTime)
            .select_from(Yinpian)
            .outerjoin(User, Yinpian.userId == User.userId)
            .where(Yinpian.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Yinpian.i1).where(Yinpian.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def get_i2(db: AsyncSession, subId: int):
        query = select(Yinpian.i2).where(Yinpian.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: Yinpian, userId: int):
        # 检查图片是否存在
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                localPath = sub.img[len("/api/"):]
                if not await os.path.isfile(localPath):
                    raise FileNotFoundError(f"{sub.title} 图片不存在")
        # 读旧的i1
        old_i1_query = select(Yinpian.i1).where(Yinpian.subId == subId)
        old_i1: Optional[List[ImageTitle]] = await db.scalar(old_i1_query)
        # 新旧比较并做处理，如果不行，则类型出了问题
        await ImageTitle.edit_compare(db, item.i1, old_i1)
        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Yinpian).where(Yinpian.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        old_i1_query = select(Yinpian.i1).where(Yinpian.subId == subId)
        old_i1: Optional[List] = await db.scalar(old_i1_query)
        if old_i1 and len(old_i1) > 0:
            for old_sub in old_i1:
                localPath = old_sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    await async_os.remove(localPath)
        query = delete(Yinpian).where(Yinpian.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "7_饮片炮制"
        query = select(Yinpian).where(Yinpian.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材基源": ImageTitle.parse_html(record.t1),
                    "药材产地": ImageTitle.parse_html(record.t2),
                    "炮制沿革": ImageTitle.parse_html(record.t3),
                    "炮制品种": ImageTitle.parse_html(record.t4),
                    "炮制工艺": ImageTitle.parse_html(record.t5),
                    "饮片性状": ImageTitle.parse_html(record.t6),
                    "成分变化": ImageTitle.parse_html(record.t7),
                    "炮制作用": ImageTitle.parse_html(record.t8),
                    "临床应用": ImageTitle.parse_html(record.t9),
                    "处方应付": ImageTitle.parse_html(record.t10),
                    "贮藏条件": ImageTitle.parse_html(record.t11),
                    "质量标准": ImageTitle.parse_html(record.t12),
                    "生品图片": f"{len(record.i1) if record.i1 else 0}张",
                    "制品图片": f"{len(record.i2) if record.i2 else 0}张"
                })
                # 处理图片，批量复制多个文件到临时目录，并重新命名
                await ImageTitle.tcm_copy_file(record.i1, temp_dir, tcmName, subName, index)
                await ImageTitle.tcm_copy_file(record.i2, temp_dir, tcmName, subName, index)
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class YinpianReq(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
    t8: Optional[str] = None
    t9: Optional[str] = None
    t10: Optional[str] = None
    t11: Optional[str] = None
    t12: Optional[str] = None
    i1: Optional[List[ImageTitle]] = []
    i2: Optional[List[ImageTitle]] = []

class YinpianQueryParams(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
    t8: Optional[str] = None
