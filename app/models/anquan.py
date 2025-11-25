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


class Anquan(Base):
    __tablename__ = "anquan"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材")
    t2 = Column(TEXT, comment="给药成分")
    t3 = Column(TEXT, comment="毒性类型")
    t4 = Column(TEXT, comment="暴露途径")
    t5 = Column(TEXT, comment="实验对象")
    t6 = Column(TEXT, comment="给药剂量范围")
    t7 = Column(TEXT, comment="半数致死剂量")
    t8 = Column(TEXT, comment="毒性发现摘要")
    t9 = Column(TEXT, comment="恢复期观察")
    t10 = Column(TEXT, comment="毒性机制")
    t11 = Column(TEXT, comment="毒性成分")
    t12 = Column(TEXT, comment="靶器官/系统")
    t13 = Column(TEXT, comment="过敏反应记录")
    t14 = Column(TEXT, comment="禁忌证")
    t15 = Column(TEXT, comment="推荐安全剂量范围")
    t16 = Column(TEXT, comment="不良反应记录")
    t17 = Column(TEXT, comment="执行标准")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: AnquanReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Anquan).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: AnquanQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Anquan.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Anquan, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Anquan.subId,
                             sql_build_start(Anquan.t1, "st1"),
                             sql_build_start(Anquan.t2, "st2"),
                             sql_build_start(Anquan.t3, "st3"),
                             sql_build_start(Anquan.t4, "st4"),
                             sql_build_start(Anquan.t5, "st5"),
                             sql_build_start(Anquan.t6, "st6"),
                             sql_build_start(Anquan.t7, "st7"),
                             sql_build_start(Anquan.t8, "st8"),
                             sql_build_start(Anquan.t9, "st9"),
                             sql_build_start(Anquan.t10, "st10"),
                             sql_build_start(Anquan.t11, "st11"),
                             sql_build_start(Anquan.t12, "st12"),
                             sql_build_start(Anquan.t13, "st13"),
                             sql_build_start(Anquan.t14, "st14"),
                             sql_build_start(Anquan.t15, "st15"),
                             sql_build_start(Anquan.t16, "st16"),
                             sql_build_start(Anquan.t17, "st17"),
                             User.userName.label("updateUser"),
                             Anquan.updateTime
                             ).outerjoin(User, Anquan.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Anquan.t1, Anquan.t2, Anquan.t3, Anquan.t4, Anquan.t5,
                   Anquan.t6, Anquan.t7, Anquan.t8, Anquan.t9, Anquan.t10,
                   Anquan.t11, Anquan.t12, Anquan.t13,
                   Anquan.t14, Anquan.t15, Anquan.t16, Anquan.t17,
                   User.userName.label("updateUser"), Anquan.updateTime)
            .select_from(Anquan)
            .outerjoin(User, Anquan.userId == User.userId)
            .where(Anquan.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: 'AnquanReq', userId: int):
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now

        # 直接更新，不过滤空值（保留空值覆盖语义）
        query = update(Anquan).where(Anquan.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        # 这里的 delete 不需要删除物理文件
        query = delete(Anquan).where(Anquan.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "文献数据"
        query = select(Anquan).where(Anquan.tcmId == tcmId)
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
                    "给药成分": ImageTitle.parse_html(record.t2),
                    "毒性类型": ImageTitle.parse_html(record.t3),
                    "暴露途径": ImageTitle.parse_html(record.t4),
                    "实验对象": ImageTitle.parse_html(record.t5),
                    "给药剂量范围": ImageTitle.parse_html(record.t6),
                    "半数致死剂量": ImageTitle.parse_html(record.t7),
                    "毒性发现摘要": ImageTitle.parse_html(record.t8),
                    "恢复期观察": ImageTitle.parse_html(record.t9),
                    "毒性机制": ImageTitle.parse_html(record.t10),
                    "毒性成分": ImageTitle.parse_html(record.t11),
                    "靶器官/系统": ImageTitle.parse_html(record.t12),
                    "过敏反应记录": ImageTitle.parse_html(record.t13),
                    "禁忌证": ImageTitle.parse_html(record.t14),
                    "推荐安全剂量范围": ImageTitle.parse_html(record.t15),
                    "不良反应记录": ImageTitle.parse_html(record.t16),
                    "执行标准": ImageTitle.parse_html(record.t17)
                })
                # 文献无需调用 ImageTitle.tcm_copy_file 复制图片
                index += 1

            # 依然调用 export_zip 生成 Excel 并压缩（即使没有图片，也会生成含 Excel 的 zip）
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class AnquanReq(BaseModel):
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


class AnquanQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t11: Optional[str] = None
    t12: Optional[str] = None
    t17: Optional[str] = None
