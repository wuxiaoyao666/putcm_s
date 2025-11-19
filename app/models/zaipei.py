import io
import tempfile
from datetime import datetime

from aiofiles import os
from sqlalchemy import Column, Integer, TEXT, JSON, BigInteger, func, insert, update, Select, delete
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .tcm import Tcm
from .tmpfile import TmpFile
from ..database import Base
from ..utils.imgutil import ImageTitle
from ..utils.listutil import ListContentLen, sql_build_start
from .user import User


class Zaipei(Base):
    __tablename__ = "zaipei"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材名称")
    t2 = Column(TEXT, comment="基原及种质")
    t3 = Column(TEXT, comment="选育品种名称")
    t4 = Column(TEXT, comment="繁育方式")
    t5 = Column(TEXT, comment="播种方式")
    t6 = Column(TEXT, comment="繁殖方式")
    t7 = Column(TEXT, comment="播种或移栽、定植时间")
    t8 = Column(TEXT, comment="田间管理措施")
    t9 = Column(TEXT, comment="大气要求")
    t10 = Column(TEXT, comment="土壤要求")
    t11 = Column(TEXT, comment="肥料使用")
    t12 = Column(TEXT, comment="病虫害防治措施")
    t13 = Column(TEXT, comment="最佳采收期")
    t14 = Column(TEXT, comment="产地加工")
    t15 = Column(TEXT, comment="产量范围")
    t16 = Column(TEXT, comment="适宜生境")
    t17 = Column(TEXT, comment="技术来源")
    t18 = Column(TEXT, comment="参考文献/标准")
    t19 = Column(TEXT, comment="备注")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: ZaipeiReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Zaipei).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: ZaipeiQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Zaipei.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Zaipei, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Zaipei.subId,
                             sql_build_start(Zaipei.t2, "st2"),
                             sql_build_start(Zaipei.t3, "st3"),
                             sql_build_start(Zaipei.t4, "st4"),
                             sql_build_start(Zaipei.t5, "st5"),
                             sql_build_start(Zaipei.t6, "st6"),
                             User.userName.label("updateUser"),
                             Zaipei.updateTime
                             ).outerjoin(User, Zaipei.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Zaipei.t1, Zaipei.t2, Zaipei.t3, Zaipei.t4, Zaipei.t5, Zaipei.t6, Zaipei.t7, Zaipei.t8, Zaipei.t9,
                   Zaipei.t10, Zaipei.t11, Zaipei.t12, Zaipei.t13, Zaipei.t14, Zaipei.t15, Zaipei.t16, Zaipei.t17,
                   Zaipei.t18, Zaipei.t19, User.userName.label("updateUser"), Zaipei.updateTime)
            .select_from(Zaipei)
            .outerjoin(User, Zaipei.userId == User.userId)
            .where(Zaipei.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: ZaipeiReq, userId: int):
        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Zaipei).where(Zaipei.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        query = delete(Zaipei).where(Zaipei.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str,str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "3_栽培（养殖）技术"
        query = select(Zaipei).where(Zaipei.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                # 处理文本字段
                excel_data.append({
                    "序号": index,
                    "药材名称":ImageTitle.parse_html(record.t1),
                    "基原及种质":ImageTitle.parse_html(record.t2),
                    "选育品种名称":ImageTitle.parse_html(record.t3),
                    "繁育方式":ImageTitle.parse_html(record.t4),
                    "播种方式":ImageTitle.parse_html(record.t5),
                    "繁殖方式":ImageTitle.parse_html(record.t6),
                    "播种或移栽、定植时间":ImageTitle.parse_html(record.t7),
                    "田间管理措施":ImageTitle.parse_html(record.t8),
                    "大气要求":ImageTitle.parse_html(record.t9),
                    "土壤要求":ImageTitle.parse_html(record.t10),
                    "肥料使用":ImageTitle.parse_html(record.t11),
                    "病虫害防治措施":ImageTitle.parse_html(record.t12),
                    "最佳采收期":ImageTitle.parse_html(record.t13),
                    "产地加工":ImageTitle.parse_html(record.t14),
                    "产量范围":ImageTitle.parse_html(record.t15),
                    "适宜生境":ImageTitle.parse_html(record.t16),
                    "技术来源":ImageTitle.parse_html(record.t17),
                    "参考文献/标准":ImageTitle.parse_html(record.t18),
                    "备注":ImageTitle.parse_html(record.t19),
                })
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName,subName, zip_buffer

class ZaipeiReq(BaseModel):
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


class ZaipeiQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
