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


class Tiqu(Base):
    __tablename__ = "tiqu"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材名称")
    t2 = Column(TEXT, comment="原植物")
    t3 = Column(TEXT, comment="提取部位")
    t4 = Column(TEXT, comment="预处理方法")
    t5 = Column(TEXT, comment="提取方式")
    t6 = Column(TEXT, comment="提取参数")
    t7 = Column(TEXT, comment="提取设备型号")
    t8 = Column(TEXT, comment="过滤方式")
    t9 = Column(TEXT, comment="过滤参数")
    t10 = Column(TEXT, comment="分离方式")
    t11 = Column(TEXT, comment="分离参数")
    t12 = Column(TEXT, comment="浓缩方式")
    t13 = Column(TEXT, comment="浓缩参数")
    t14 = Column(TEXT, comment="干燥方式")
    t15 = Column(TEXT, comment="干燥参数")
    t16 = Column(TEXT, comment="最终产物形态")
    t17 = Column(TEXT, comment="得率（%）")
    t18 = Column(TEXT, comment="工艺规模")
    t19 = Column(TEXT, comment="目标成分名称")
    t20 = Column(TEXT, comment="目标成分要求")
    t21 = Column(TEXT, comment="目标成分检测方法依据")
    i1 = Column(JSON, comment="相关图谱（list，{img,title}")
    t22 = Column(TEXT, comment="工艺来源")
    t23 = Column(TEXT, comment="引用文献/说明书")
    t24 = Column(TEXT, comment="备注说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: TiquReq, userId: int):
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
        query = insert(Tiqu).values(**values)
        await db.execute(query)
        await db.commit()
        # 删除临时文件记录
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                await TmpFile.delRecord(db, sub.img)

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: TiquQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Tiqu.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Tiqu, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Tiqu.subId,
                             sql_build_start(Tiqu.t2, "st2"),
                             sql_build_start(Tiqu.t3, "st3"),
                             sql_build_start(Tiqu.t4, "st4"),
                             sql_build_start(Tiqu.t5, "st5"),
                             sql_build_start(Tiqu.t8, "st8"),
                             sql_build_start(Tiqu.t10, "st10"),
                             sql_build_start(Tiqu.t19, "st19"),
                             User.userName.label("updateUser"),
                             Tiqu.updateTime
                             ).outerjoin(User, Tiqu.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Tiqu.t1, Tiqu.t2, Tiqu.t3, Tiqu.t4, Tiqu.t5, Tiqu.t6, Tiqu.t7, Tiqu.t8, Tiqu.t9, Tiqu.t10, Tiqu.t11,
                   Tiqu.t12, Tiqu.t13, Tiqu.t14, Tiqu.t15, Tiqu.t16, Tiqu.t17, Tiqu.t18, Tiqu.t19, Tiqu.t20, Tiqu.t21,
                   func.JSON_LENGTH(Tiqu.i1).label("si1"), Tiqu.t22, Tiqu.t23, Tiqu.t24,
                   User.userName.label("updateUser"), Tiqu.updateTime)
            .select_from(Tiqu)
            .outerjoin(User, Tiqu.userId == User.userId)
            .where(Tiqu.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Tiqu.i1).where(Tiqu.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: TiquReq, userId: int):
        # 检查图片是否存在
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                localPath = sub.img[len("/api/"):]
                if not await os.path.isfile(localPath):
                    raise FileNotFoundError(f"{sub.title} 图片不存在")
        # 读旧的i1
        old_i1_query = select(Tiqu.i1).where(Tiqu.subId == subId)
        old_i1: Optional[List[ImageTitle]] = await db.scalar(old_i1_query)
        # 新旧比较并做处理，如果不行，则类型出了问题
        await ImageTitle.edit_compare(db, item.i1, old_i1)
        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Tiqu).where(Tiqu.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        old_i1_query = select(Tiqu.i1).where(Tiqu.subId == subId)
        old_i1: Optional[List] = await db.scalar(old_i1_query)
        if old_i1 and len(old_i1) > 0:
            for old_sub in old_i1:
                localPath = old_sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    await async_os.remove(localPath)
        query = delete(Tiqu).where(Tiqu.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "4_提取分离"
        query = select(Tiqu).where(Tiqu.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材名称": ImageTitle.parse_html(record.t1),
                    "原植物": ImageTitle.parse_html(record.t2),
                    "提取部位": ImageTitle.parse_html(record.t3),
                    "预处理方法": ImageTitle.parse_html(record.t4),
                    "提取方式": ImageTitle.parse_html(record.t5),
                    "提取参数": ImageTitle.parse_html(record.t6),
                    "提取设备型号": ImageTitle.parse_html(record.t7),
                    "过滤方式": ImageTitle.parse_html(record.t8),
                    "过滤参数": ImageTitle.parse_html(record.t9),
                    "分离方式": ImageTitle.parse_html(record.t10),
                    "分离参数": ImageTitle.parse_html(record.t11),
                    "浓缩方式": ImageTitle.parse_html(record.t12),
                    "浓缩参数": ImageTitle.parse_html(record.t13),
                    "干燥方式": ImageTitle.parse_html(record.t14),
                    "干燥参数": ImageTitle.parse_html(record.t15),
                    "最终产物形态": ImageTitle.parse_html(record.t16),
                    "得率（%）": ImageTitle.parse_html(record.t17),
                    "工艺规模": ImageTitle.parse_html(record.t18),
                    "目标成分名称": ImageTitle.parse_html(record.t19),
                    "目标成分要求": ImageTitle.parse_html(record.t20),
                    "目标成分检测方法依据": ImageTitle.parse_html(record.t21),
                    "相关图谱": f"{len(record.i1) if record.i1 else 0}张",
                    "工艺来源": ImageTitle.parse_html(record.t22),
                    "引用文献/说明书": ImageTitle.parse_html(record.t23),
                    "备注说明": ImageTitle.parse_html(record.t24),
                })
                # 处理图片，批量复制多个文件到临时目录，并重新命名
                await ImageTitle.tcm_copy_file(record.i1, temp_dir, tcmName, subName, index)
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class TiquReq(BaseModel):
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
    t13: Optional[str] = None
    t14: Optional[str] = None
    t15: Optional[str] = None
    t16: Optional[str] = None
    t17: Optional[str] = None
    t18: Optional[str] = None
    t19: Optional[str] = None
    t20: Optional[str] = None
    t21: Optional[str] = None
    i1: Optional[List[ImageTitle]] = []
    t22: Optional[str] = None
    t23: Optional[str] = None
    t24: Optional[str] = None


class TiquQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t8: Optional[str] = None
    t10: Optional[str] = None
    t19: Optional[str] = None
