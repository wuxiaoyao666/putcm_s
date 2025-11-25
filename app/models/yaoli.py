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

class Yaoli(Base):
    __tablename__ = "yaoli"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t16 = Column(TEXT, comment="药材")
    t1 = Column(TEXT, comment="药理作用类型")
    t2 = Column(TEXT, comment="药效成分")
    t3 = Column(TEXT, comment="靶点蛋白")
    t4 = Column(TEXT, comment="信号通路")
    t5 = Column(TEXT, comment="模型类型")
    t6 = Column(TEXT, comment="实验对象")
    t7 = Column(TEXT, comment="给药信息")
    t8 = Column(TEXT, comment="药效指标变化")
    t9 = Column(TEXT, comment="有效浓度(IC₅₀/EC₅₀等)")
    t10 = Column(TEXT, comment="毒性/副作用评价")
    t11 = Column(TEXT, comment="对照组情况")
    t12 = Column(TEXT, comment="总结结论")
    t13 = Column(TEXT, comment="文献/数据来源")
    t14 = Column(TEXT, comment="录入人员")
    t15 = Column(TEXT, comment="审核人员")
    t17 = Column(TEXT, comment="备注")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: YaoliReq, userId: int):

        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Yaoli).values(**values)
        await db.execute(query)
        await db.commit()


    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: YaoliQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Yaoli.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Yaoli, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Yaoli.subId,
                             sql_build_start(Yaoli.t1, "st1"),
                             sql_build_start(Yaoli.t2, "st2"),
                             sql_build_start(Yaoli.t4, "st4"),
                             sql_build_start(Yaoli.t5, "st5"),
                             sql_build_start(Yaoli.t6, "st6"),
                             sql_build_start(Yaoli.t7, "st7"),
                             sql_build_start(Yaoli.t8, "st8"),
                             User.userName.label("updateUser"),
                             Yaoli.updateTime
                             ).outerjoin(User, Yaoli.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Yaoli.t16, Yaoli.t1, Yaoli.t2, Yaoli.t3, Yaoli.t4, Yaoli.t5, Yaoli.t6, Yaoli.t7, Yaoli.t8, Yaoli.t9, Yaoli.t10, Yaoli.t11,
                   Yaoli.t12, Yaoli.t13, Yaoli.t14, Yaoli.t15,Yaoli.t17,
                   User.userName.label("updateUser"), Yaoli.updateTime)
            .select_from(Yaoli)
            .outerjoin(User, Yaoli.userId == User.userId)
            .where(Yaoli.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Yaoli.i1).where(Yaoli.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: Yaoli, userId: int):

        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Yaoli).where(Yaoli.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        query = delete(Yaoli).where(Yaoli.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "8_质量分析"
        query = select(Yaoli).where(Yaoli.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材": ImageTitle.parse_html(record.t16),
                    "药理作用类型": ImageTitle.parse_html(record.t1),
                    "药效成分": ImageTitle.parse_html(record.t2),
                    "靶点蛋白": ImageTitle.parse_html(record.t3),
                    "信号通路": ImageTitle.parse_html(record.t4),
                    "模型类型": ImageTitle.parse_html(record.t5),
                    "实验对象": ImageTitle.parse_html(record.t6),
                    "给药信息": ImageTitle.parse_html(record.t7),
                    "药效指标变化": ImageTitle.parse_html(record.t8),
                    "有效浓度(IC₅₀/EC₅₀等)": ImageTitle.parse_html(record.t9),
                    "毒性/副作用评价": ImageTitle.parse_html(record.t10),
                    "对照组情况": ImageTitle.parse_html(record.t11),
                    "总结结论": ImageTitle.parse_html(record.t12),
                    "文献/数据来源": ImageTitle.parse_html(record.t13),
                    "录入人员": ImageTitle.parse_html(record.t14),
                    "审核人员": ImageTitle.parse_html(record.t15),
                    "备注": ImageTitle.parse_html(record.t17),
                })
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class YaoliReq(BaseModel):
    t16: Optional[str] = None
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
    t17: Optional[str] = None

class YaoliQueryParams(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
