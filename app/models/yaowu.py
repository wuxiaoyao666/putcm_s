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


class Yaowu(Base):
    __tablename__ = 'yaowu'
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材")
    t2 = Column(TEXT, comment="给药成分")
    t3 = Column(TEXT, comment="给药途径")
    t4 = Column(TEXT, comment="给药剂量")
    t5 = Column(TEXT, comment="研究对象")
    t6 = Column(TEXT, comment="检测对象")
    t7 = Column(TEXT, comment="吸收特征")
    t8 = Column(TEXT, comment="达峰时间（Tmax）")
    t9 = Column(TEXT, comment="峰浓度（Cmax）")
    t10 = Column(TEXT, comment="半衰期（t½）")
    t11 = Column(TEXT, comment="曲线下面积（AUC(0-t)）")
    t12 = Column(TEXT, comment="曲线下面积（AUC(0-∞)）")
    t13 = Column(TEXT, comment="表观分布容积（Vd）")
    t14 = Column(TEXT, comment="平均滞留时间（MRT）")
    t15 = Column(TEXT, comment="清除率（CL）")
    t16 = Column(TEXT, comment="生物利用度（F%）")
    t17 = Column(TEXT, comment="分布特征")
    t18 = Column(TEXT, comment="主要代谢产物及路径")
    t19 = Column(TEXT, comment="排泄路径")
    t20 = Column(TEXT, comment="测定方法")
    t21 = Column(TEXT, comment="数据来源")
    t22 = Column(TEXT, comment="备注说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: YaowuReq, userId: int):
        # 转换为有效的dict，去掉None值
        values = item.model_dump()  # exclude_none=True)，之前做了排除none值，后来发现没必要
        values['tcmId'] = tcmId
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now
        query = insert(Yaowu).values(**values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: YaowuQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Yaowu.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Yaowu, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Yaowu.subId,
                             sql_build_start(Yaowu.t1, "st1"),
                             sql_build_start(Yaowu.t2, "st2"),
                             sql_build_start(Yaowu.t3, "st3"),
                             sql_build_start(Yaowu.t4, "st4"),
                             sql_build_start(Yaowu.t5, "st5"),
                             sql_build_start(Yaowu.t6, "st6"),
                             sql_build_start(Yaowu.t7, "st7"),
                             sql_build_start(Yaowu.t8, "st8"),
                             sql_build_start(Yaowu.t9, "st9"),
                             sql_build_start(Yaowu.t10, "st10"),
                             sql_build_start(Yaowu.t11, "st11"),
                             sql_build_start(Yaowu.t12, "st12"),
                             sql_build_start(Yaowu.t13, "st13"),
                             sql_build_start(Yaowu.t14, "st14"),
                             sql_build_start(Yaowu.t15, "st15"),
                             sql_build_start(Yaowu.t16, "st16"),
                             sql_build_start(Yaowu.t17, "st17"),
                             sql_build_start(Yaowu.t18, "st18"),
                             sql_build_start(Yaowu.t19, "st19"),
                             sql_build_start(Yaowu.t20, "st20"),
                             sql_build_start(Yaowu.t21, "st21"),
                             sql_build_start(Yaowu.t22, "st22"),
                             User.userName.label("updateUser"),
                             Yaowu.updateTime
                             ).outerjoin(User, Yaowu.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Yaowu.t1, Yaowu.t2, Yaowu.t3, Yaowu.t4, Yaowu.t5,
                   Yaowu.t6, Yaowu.t7, Yaowu.t8, Yaowu.t9, Yaowu.t10,
                   Yaowu.t11, Yaowu.t12, Yaowu.t13,
                   Yaowu.t14, Yaowu.t15, Yaowu.t16,
                   Yaowu.t17, Yaowu.t18, Yaowu.t19,
                   Yaowu.t20, Yaowu.t21, Yaowu.t22,
                   User.userName.label("updateUser"), Yaowu.updateTime)
            .select_from(Yaowu)
            .outerjoin(User, Yaowu.userId == User.userId)
            .where(Yaowu.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: 'YaowuReq', userId: int):
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now

        # 直接更新，不过滤空值（保留空值覆盖语义）
        query = update(Yaowu).where(Yaowu.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        # 这里的 delete 不需要删除物理文件
        query = delete(Yaowu).where(Yaowu.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "开发利用"
        query = select(Yaowu).where(Yaowu.tcmId == tcmId)
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
                    "给药途径": ImageTitle.parse_html(record.t3),
                    "给药剂量": ImageTitle.parse_html(record.t4),
                    "研究对象": ImageTitle.parse_html(record.t5),
                    "检测对象": ImageTitle.parse_html(record.t6),
                    "吸收特征": ImageTitle.parse_html(record.t7),
                    "达峰时间（Tmax）": ImageTitle.parse_html(record.t8),
                    "峰浓度（Cmax）": ImageTitle.parse_html(record.t9),
                    "半衰期（t½）": ImageTitle.parse_html(record.t10),
                    "曲线下面积（AUC(0-t)）": ImageTitle.parse_html(record.t11),
                    "曲线下面积（AUC(0-∞)）": ImageTitle.parse_html(record.t12),
                    "表观分布容积（Vd）": ImageTitle.parse_html(record.t13),
                    "平均滞留时间（MRT）": ImageTitle.parse_html(record.t14),
                    "清除率（CL）": ImageTitle.parse_html(record.t15),
                    "生物利用度（F%）": ImageTitle.parse_html(record.t16),
                    "分布特征": ImageTitle.parse_html(record.t17),
                    "代谢产物": ImageTitle.parse_html(record.t18),
                    "排泄路径": ImageTitle.parse_html(record.t19),
                    "测定方法": ImageTitle.parse_html(record.t20),
                    "数据来源": ImageTitle.parse_html(record.t21),
                    "备注说明": ImageTitle.parse_html(record.t22),
                })
                # 文献无需调用 ImageTitle.tcm_copy_file 复制图片
                index += 1

            # 依然调用 export_zip 生成 Excel 并压缩（即使没有图片，也会生成含 Excel 的 zip）
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class YaowuReq(BaseModel):
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


class YaowuQueryParams(BaseModel):
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t18: Optional[str] = None
    t20: Optional[str] = None
