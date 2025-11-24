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


class Wenxian(Base):
    __tablename__ = 'wenxian'
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材")
    t2 = Column(TEXT, comment="文献标题")
    t3 = Column(TEXT, comment="文献类型")
    t4 = Column(TEXT, comment="作者/主编")
    t5 = Column(TEXT, comment="文献来源")
    t6 = Column(TEXT, comment="发表/出版年份")
    t7 = Column(TEXT, comment="期刊信息")
    t8 = Column(TEXT, comment="DOI链接/PDF")
    t9 = Column(TEXT, comment="文献语言")
    t10 = Column(TEXT, comment="关键词")
    t11 = Column(TEXT, comment="摘要")
    t12 = Column(TEXT, comment="引用用途分类")
    t13 = Column(TEXT, comment="补充说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: WenxianReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Wenxian).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: WenxianQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Wenxian.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Wenxian, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Wenxian.subId,
                             sql_build_start(Wenxian.t1, "st1"),
                             sql_build_start(Wenxian.t2, "st2"),
                             sql_build_start(Wenxian.t3, "st3"),
                             sql_build_start(Wenxian.t4, "st4"),
                             sql_build_start(Wenxian.t5, "st5"),
                             sql_build_start(Wenxian.t6, "st6"),
                             sql_build_start(Wenxian.t7, "st7"),
                             sql_build_start(Wenxian.t8, "st8"),
                             sql_build_start(Wenxian.t9, "st9"),
                             sql_build_start(Wenxian.t10, "st10"),
                             sql_build_start(Wenxian.t11, "st11"),
                             sql_build_start(Wenxian.t12, "st12"),
                             sql_build_start(Wenxian.t13, "st13"),
                             User.userName.label("updateUser"),
                             Wenxian.updateTime
                             ).outerjoin(User, Wenxian.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Wenxian.t1, Wenxian.t2, Wenxian.t3, Wenxian.t4, Wenxian.t5,
                   Wenxian.t6, Wenxian.t7, Wenxian.t8, Wenxian.t9, Wenxian.t10,
                   Wenxian.t11, Wenxian.t12, Wenxian.t13,
                   User.userName.label("updateUser"), Wenxian.updateTime)
            .select_from(Wenxian)
            .outerjoin(User, Wenxian.userId == User.userId)
            .where(Wenxian.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: 'WenxianReq', userId: int):
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now

        # 直接更新，不过滤空值（保留空值覆盖语义）
        query = update(Wenxian).where(Wenxian.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        # 这里的 delete 不需要删除物理文件
        query = delete(Wenxian).where(Wenxian.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "文献数据"
        query = select(Wenxian).where(Wenxian.tcmId == tcmId)
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
                    "文献标题": ImageTitle.parse_html(record.t2),
                    "文献类型": ImageTitle.parse_html(record.t3),
                    "作者/主编": ImageTitle.parse_html(record.t4),
                    "文献来源": ImageTitle.parse_html(record.t5),
                    "发表/出版年份": ImageTitle.parse_html(record.t6),
                    "期刊信息": ImageTitle.parse_html(record.t7),
                    "DOI链接/PDF": ImageTitle.parse_html(record.t8),
                    "文献语言": ImageTitle.parse_html(record.t9),
                    "关键词": ImageTitle.parse_html(record.t10),
                    "摘要": ImageTitle.parse_html(record.t11),
                    "引用用途分类": ImageTitle.parse_html(record.t12),
                    "补充说明": ImageTitle.parse_html(record.t13)
                })
                # 文献无需调用 ImageTitle.tcm_copy_file 复制图片
                index += 1

            # 依然调用 export_zip 生成 Excel 并压缩（即使没有图片，也会生成含 Excel 的 zip）
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class WenxianReq(BaseModel):
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


class WenxianQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
