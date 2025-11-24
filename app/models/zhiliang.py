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

class Zhiliang(Base):
    __tablename__ = "zhiliang"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材")
    t2 = Column(TEXT, comment="药材编号")
    t3 = Column(TEXT, comment="检测部位")
    t4 = Column(TEXT, comment="样品状态")
    t5 = Column(TEXT, comment="检测标准")
    t6 = Column(TEXT, comment="鉴别方法")
    t7 = Column(TEXT, comment="检测目标")
    t8 = Column(TEXT, comment="测定方法")
    t9 = Column(TEXT, comment="方法参数详情")
    t10 = Column(TEXT, comment="标准曲线方程")
    t11 = Column(TEXT, comment="含量限度")
    t12 = Column(TEXT, comment="检测结果")
    t13 = Column(TEXT, comment="判定标准")
    t14 = Column(TEXT, comment="仪器型号")
    t15 = Column(TEXT, comment="检测人员")
    t16 = Column(TEXT, comment="检测机构")
    t17 = Column(TEXT, comment="备注说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: ZhiliangReq, userId: int):

        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Zhiliang).values(**values)
        await db.execute(query)
        await db.commit()


    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: ZhiliangQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Zhiliang.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Zhiliang, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Zhiliang.subId,
                             sql_build_start(Zhiliang.t2, "st2"),
                             sql_build_start(Zhiliang.t3, "st3"),
                             sql_build_start(Zhiliang.t4, "st4"),
                             sql_build_start(Zhiliang.t5, "st5"),
                             sql_build_start(Zhiliang.t6, "st6"),
                             sql_build_start(Zhiliang.t7, "st7"),
                             sql_build_start(Zhiliang.t8, "st8"),
                             User.userName.label("updateUser"),
                             Zhiliang.updateTime
                             ).outerjoin(User, Zhiliang.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Zhiliang.t1, Zhiliang.t2, Zhiliang.t3, Zhiliang.t4, Zhiliang.t5, Zhiliang.t6, Zhiliang.t7, Zhiliang.t8, Zhiliang.t9, Zhiliang.t10, Zhiliang.t11,
                   Zhiliang.t12, Zhiliang.t13, Zhiliang.t14, Zhiliang.t15, Zhiliang.t16, Zhiliang.t17,
                   User.userName.label("updateUser"), Zhiliang.updateTime)
            .select_from(Zhiliang)
            .outerjoin(User, Zhiliang.userId == User.userId)
            .where(Zhiliang.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Zhiliang.i1).where(Zhiliang.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: Zhiliang, userId: int):

        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Zhiliang).where(Zhiliang.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        query = delete(Zhiliang).where(Zhiliang.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "6_质量分析"
        query = select(Zhiliang).where(Zhiliang.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材": ImageTitle.parse_html(record.t1),
                    "药材编号": ImageTitle.parse_html(record.t2),
                    "检测部位": ImageTitle.parse_html(record.t3),
                    "样品状态": ImageTitle.parse_html(record.t4),
                    "检测标准": ImageTitle.parse_html(record.t5),
                    "鉴别方法": ImageTitle.parse_html(record.t6),
                    "检测目标": ImageTitle.parse_html(record.t7),
                    "测定方法": ImageTitle.parse_html(record.t8),
                    "方法参数详情": ImageTitle.parse_html(record.t9),
                    "标准曲线方程": ImageTitle.parse_html(record.t10),
                    "含量限度": ImageTitle.parse_html(record.t11),
                    "检测结果": ImageTitle.parse_html(record.t12),
                    "判定标准": ImageTitle.parse_html(record.t13),
                    "仪器型号": ImageTitle.parse_html(record.t14),
                    "检测人员": ImageTitle.parse_html(record.t15),
                    "检测机构": ImageTitle.parse_html(record.t16),
                    "备注说明": ImageTitle.parse_html(record.t17),
                })
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class ZhiliangReq(BaseModel):
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

class ZhiliangQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
    t8: Optional[str] = None
