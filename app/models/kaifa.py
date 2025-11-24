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


class Kaifa(Base):
    __tablename__ = 'kaifa'
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材名称")
    t2 = Column(TEXT, comment="产品名称")
    t3 = Column(TEXT, comment="产品类别")
    t4 = Column(TEXT, comment="剂型")
    t5 = Column(TEXT, comment="配方组成")
    t6 = Column(TEXT, comment="规格")
    t7 = Column(TEXT, comment="食用方法")
    t8 = Column(TEXT, comment="过敏原信息")
    t9 = Column(TEXT, comment="禁忌")
    t10 = Column(TEXT, comment="储存条件")
    t11 = Column(TEXT, comment="功能主治")
    t12 = Column(TEXT, comment="适用症")
    t13 = Column(TEXT, comment="注册上市情况")
    t14 = Column(TEXT, comment="注册号/批准文号")
    t15 = Column(TEXT, comment="开发单位/上市许可持有人")
    t16 = Column(TEXT, comment="生产工艺概述")
    t17 = Column(TEXT, comment="得率/收率指标")
    t18 = Column(TEXT, comment="知识产权")
    t19 = Column(TEXT, comment="参考资料")
    t20 = Column(TEXT, comment="资源综合利用方式")
    t21 = Column(TEXT, comment="市场区域/销售国家")
    t22 = Column(TEXT, comment="年产量/年销售量")
    t23 = Column(TEXT, comment="效果/用户评价摘要")
    t24 = Column(TEXT, comment="补充说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: KaifaReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Kaifa).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: KaifaQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Kaifa.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Kaifa, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Kaifa.subId,
                             sql_build_start(Kaifa.t1, "st1"),
                             sql_build_start(Kaifa.t2, "st2"),
                             sql_build_start(Kaifa.t3, "st3"),
                             sql_build_start(Kaifa.t4, "st4"),
                             sql_build_start(Kaifa.t5, "st5"),
                             sql_build_start(Kaifa.t6, "st6"),
                             sql_build_start(Kaifa.t7, "st7"),
                             sql_build_start(Kaifa.t8, "st8"),
                             sql_build_start(Kaifa.t9, "st9"),
                             sql_build_start(Kaifa.t10, "st10"),
                             sql_build_start(Kaifa.t11, "st11"),
                             sql_build_start(Kaifa.t12, "st12"),
                             sql_build_start(Kaifa.t13, "st13"),
                             sql_build_start(Kaifa.t14, "st14"),
                             sql_build_start(Kaifa.t15, "st15"),
                             sql_build_start(Kaifa.t16, "st16"),
                             sql_build_start(Kaifa.t17, "st17"),
                             sql_build_start(Kaifa.t18, "st18"),
                             sql_build_start(Kaifa.t19, "st19"),
                             sql_build_start(Kaifa.t20, "st20"),
                             sql_build_start(Kaifa.t21, "st21"),
                             sql_build_start(Kaifa.t22, "st22"),
                             sql_build_start(Kaifa.t23, "st23"),
                             sql_build_start(Kaifa.t24, "st24"),
                             User.userName.label("updateUser"),
                             Kaifa.updateTime
                             ).outerjoin(User, Kaifa.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Kaifa.t1, Kaifa.t2, Kaifa.t3, Kaifa.t4, Kaifa.t5,
                   Kaifa.t6, Kaifa.t7, Kaifa.t8, Kaifa.t9, Kaifa.t10,
                   Kaifa.t11, Kaifa.t12, Kaifa.t13,
                   Kaifa.t14, Kaifa.t15, Kaifa.t16,
                   Kaifa.t17, Kaifa.t18, Kaifa.t19,
                   Kaifa.t20, Kaifa.t21, Kaifa.t22,
                   Kaifa.t23, Kaifa.t24,
                   User.userName.label("updateUser"), Kaifa.updateTime)
            .select_from(Kaifa)
            .outerjoin(User, Kaifa.userId == User.userId)
            .where(Kaifa.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: 'KaifaReq', userId: int):
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now

        # 直接更新，不过滤空值（保留空值覆盖语义）
        query = update(Kaifa).where(Kaifa.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        # 这里的 delete 不需要删除物理文件
        query = delete(Kaifa).where(Kaifa.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "开发利用"
        query = select(Kaifa).where(Kaifa.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                # 将所有字段映射到 Excel 列
                excel_data.append({
                    "序号": index,
                    "药材名称": ImageTitle.parse_html(record.t1),
                    "产品名称": ImageTitle.parse_html(record.t2),
                    "产品类别": ImageTitle.parse_html(record.t3),
                    "剂型": ImageTitle.parse_html(record.t4),
                    "配方组成": ImageTitle.parse_html(record.t5),
                    "规格": ImageTitle.parse_html(record.t6),
                    "食用方法": ImageTitle.parse_html(record.t7),
                    "过敏原信息": ImageTitle.parse_html(record.t8),
                    "禁忌": ImageTitle.parse_html(record.t9),
                    "储存条件": ImageTitle.parse_html(record.t10),
                    "功能主治": ImageTitle.parse_html(record.t11),
                    "适用症": ImageTitle.parse_html(record.t12),
                    "注册上市情况": ImageTitle.parse_html(record.t13),
                    "注册号/批准文号": ImageTitle.parse_html(record.t14),
                    "开发单位/上市许可持有人": ImageTitle.parse_html(record.t15),
                    "生产工艺概述": ImageTitle.parse_html(record.t16),
                    "得率/收率指标": ImageTitle.parse_html(record.t17),
                    "知识产权": ImageTitle.parse_html(record.t18),
                    "参考资料": ImageTitle.parse_html(record.t19),
                    "资源综合利用方式": ImageTitle.parse_html(record.t20),
                    "市场区域/销售国家": ImageTitle.parse_html(record.t21),
                    "年产量/年销售量": ImageTitle.parse_html(record.t22),
                    "效果/用户评价摘要": ImageTitle.parse_html(record.t23),
                    "补充说明": ImageTitle.parse_html(record.t24)
                })
                # 文献无需调用 ImageTitle.tcm_copy_file 复制图片
                index += 1

            # 依然调用 export_zip 生成 Excel 并压缩（即使没有图片，也会生成含 Excel 的 zip）
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class KaifaReq(BaseModel):
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
    t22: Optional[str] = None
    t23: Optional[str] = None
    t24: Optional[str] = None


class KaifaQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t11: Optional[str] = None
    t12: Optional[str] = None
