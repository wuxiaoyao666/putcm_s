import io
import tempfile
from datetime import datetime

from sqlalchemy import Column, Integer, TEXT, BigInteger, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field
from typing import Optional, Annotated, Tuple

from .tcm import Tcm
from ..database import Base
from .user import User
from ..utils.imgutil import ImageTitle

TcmType = {1: "植物药", 2: "动物药", 3: "矿物药", 4: "其他"}


class Bencao(Base):
    __tablename__ = "bencao"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材名称")
    tcmType = Column(Integer, comment="药物类型，1-植物药，2-动物药，3-矿物药，4-其他")
    t2 = Column(TEXT, comment="本草记载")
    t3 = Column(TEXT, comment="名称考证")
    t4 = Column(TEXT, comment="基原考证")
    t5 = Column(TEXT, comment="药用部件考证")
    t6 = Column(TEXT, comment="产地考证")
    t7 = Column(TEXT, comment="性味归经考证")
    t8 = Column(TEXT, comment="功能主治考证")
    t9 = Column(TEXT, comment="用法用量考证")
    t10 = Column(TEXT, comment="备注")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def get(db: AsyncSession, tcmId: int):
        query = (select(Bencao.t1, Bencao.tcmType, Bencao.t2, Bencao.t3, Bencao.t4, Bencao.t5, Bencao.t6, Bencao.t7,
                        Bencao.t8, Bencao.t9, Bencao.t10, Bencao.updateTime, User.userName.label("updateUser"))
                 .select_from(Bencao)
                 .outerjoin(User, Bencao.userId == User.userId)
                 .where(Bencao.tcmId == tcmId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def edit(db: AsyncSession, tcmId: int, item: BencaoReq, userId: int):
        """插入或更新数据"""
        count_query = select(func.count()).where(Bencao.tcmId == tcmId).select_from(Bencao)
        count_res = await db.execute(count_query)
        count = count_res.scalar()

        # 转换为有效的dict，去掉None值
        values = item.model_dump(exclude_none=True)
        # 增加通用字段
        values["userId"] = userId
        now = int(datetime.now().timestamp())
        values["insertTime"] = now
        values["updateTime"] = now

        if count > 0:  # 编辑
            edit_query = update(Bencao).where(Bencao.tcmId == tcmId).values(**values)
        else:  # 插入
            values["tcmId"] = tcmId
            edit_query = insert(Bencao).values(**values)
        await db.execute(edit_query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str,str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "1_本草考证"
        query = select(Bencao).where(Bencao.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材名称": ImageTitle.parse_html(record.t1),
                    "药物类型": TcmType.get(record.tcmType),
                    "本草记载": ImageTitle.parse_html(record.t2),
                    "名称考证": ImageTitle.parse_html(record.t3),
                    "基原考证": ImageTitle.parse_html(record.t4),
                    "药用部位考证": ImageTitle.parse_html(record.t5),
                    "产地考证": ImageTitle.parse_html(record.t6),
                    "性味归经考证": ImageTitle.parse_html(record.t7),
                    "功能主治考证": ImageTitle.parse_html(record.t8),
                    "用法用量考证": ImageTitle.parse_html(record.t9),
                    "备注": ImageTitle.parse_html(record.t10),
                })
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName,subName, zip_buffer


class BencaoReq(BaseModel):
    t1: Optional[str] = None
    tcmType: Annotated[int, Field(ge=1, le=4)]  # v2现代写法
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    t7: Optional[str] = None
    t8: Optional[str] = None
    t9: Optional[str] = None
    t10: Optional[str] = None
