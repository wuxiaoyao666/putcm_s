import io
import tempfile
from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, TEXT, BigInteger, insert, Select, select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .tcm import Tcm
from .. import User
from ..database import Base
from ..utils.imgutil import ImageTitle
from ..utils.listutil import sql_build_start


class Linchuang(Base):
    __tablename__ = 'linchuang'
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材")
    t2 = Column(TEXT, comment="饮片")
    t3 = Column(TEXT, comment="功能主治")
    t4 = Column(TEXT, comment="用法用量")
    t5 = Column(TEXT, comment="常用方剂")
    t6 = Column(TEXT, comment="中成药")
    t7 = Column(TEXT, comment="临床应用")
    t8 = Column(TEXT, comment="中西联合用药")
    t9 = Column(TEXT, comment="不良反应")
    t10 = Column(TEXT, comment="备注")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: LinchuangReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Linchuang).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: LinchuangQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Linchuang.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Linchuang, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Linchuang.subId,
                             sql_build_start(Linchuang.t1, "st1"),
                             sql_build_start(Linchuang.t2, "st2"),
                             sql_build_start(Linchuang.t3, "st3"),
                             sql_build_start(Linchuang.t4, "st4"),
                             sql_build_start(Linchuang.t5, "st5"),
                             sql_build_start(Linchuang.t6, "st6"),
                             sql_build_start(Linchuang.t7, "st7"),
                             sql_build_start(Linchuang.t8, "st8"),
                             sql_build_start(Linchuang.t9, "st9"),
                             sql_build_start(Linchuang.t10, "st10"),
                             User.userName.label("updateUser"),
                             Linchuang.updateTime
                             ).outerjoin(User, Linchuang.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Linchuang.t1, Linchuang.t2, Linchuang.t3, Linchuang.t4, Linchuang.t5,
                   Linchuang.t6, Linchuang.t7, Linchuang.t8, Linchuang.t9,
                   User.userName.label("updateUser"), Linchuang.updateTime)
            .select_from(Linchuang)
            .outerjoin(User, Linchuang.userId == User.userId)
            .where(Linchuang.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: 'LinchuangReq', userId: int):
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now

        # 直接更新，不过滤空值（保留空值覆盖语义）
        query = update(Linchuang).where(Linchuang.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        # 这里的 delete 不需要删除物理文件
        query = delete(Linchuang).where(Linchuang.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "临床应用"
        query = select(Linchuang).where(Linchuang.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                # 将所有字段映射到 Excel 列
                excel_data.append({
                    "序号": index,
                    "药材": ImageTitle.parse_html(record.t1),
                    "饮片": ImageTitle.parse_html(record.t2),
                    "功能主治": ImageTitle.parse_html(record.t3),
                    "用法用量": ImageTitle.parse_html(record.t4),
                    "常用方剂": ImageTitle.parse_html(record.t5),
                    "中成药": ImageTitle.parse_html(record.t6),
                    "临床应用": ImageTitle.parse_html(record.t7),
                    "中西联合用药": ImageTitle.parse_html(record.t8),
                    "不良反应": ImageTitle.parse_html(record.t9),
                    "备注": ImageTitle.parse_html(record.t10),
                })
                # 文献无需调用 ImageTitle.tcm_copy_file 复制图片
                index += 1

            # 依然调用 export_zip 生成 Excel 并压缩（即使没有图片，也会生成含 Excel 的 zip）
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class LinchuangReq(BaseModel):
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


class LinchuangQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
    t8: Optional[str] = None
