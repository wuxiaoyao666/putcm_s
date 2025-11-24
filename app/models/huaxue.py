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

class Huaxue(Base):
    __tablename__ = "huaxue"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材来源")
    t2 = Column(TEXT, comment="来源部位")
    t3 = Column(TEXT, comment="药材编号")
    t4 = Column(TEXT, comment="化合物名称")
    t5 = Column(TEXT, comment="化合物描述")
    t6 = Column(TEXT, comment="英文名称")
    t7 = Column(TEXT, comment="分子式")
    t8 = Column(TEXT, comment="分子量（g/mol）")
    t9 = Column(TEXT, comment="SMILES结构式")
    i1 = Column(JSON, comment="分子结构图（list，{img,title}")
    t10 = Column(TEXT, comment="理化性质")
    t11 = Column(TEXT, comment="化学结构分类")
    t12 = Column(TEXT, comment="紫外（UV）光谱")
    t13 = Column(TEXT, comment="红外（IR）光谱")
    t14 = Column(TEXT, comment="圆二色（CD）光谱")
    t15 = Column(TEXT, comment="核磁共振氢谱（1H NMR）")
    t16 = Column(TEXT, comment="核磁共振碳谱（13C NMR）")
    t17 = Column(TEXT, comment="提取方式")
    t18 = Column(TEXT, comment="含量范围（%或mg/g）")
    t19 = Column(TEXT, comment="含量变化因素")
    t20 = Column(TEXT, comment="药理活性描述")
    t21 = Column(TEXT, comment="作用靶点/通路")
    t22 = Column(TEXT, comment="文献/数据库来源")
    t23 = Column(TEXT, comment="备注说明")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: HuaxueReq, userId: int):
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
        query = insert(Huaxue).values(**values)
        await db.execute(query)
        await db.commit()
        # 删除临时文件记录
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                await TmpFile.delRecord(db, sub.img)

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: HuaxueQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Huaxue.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Huaxue, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Huaxue.subId,
                             sql_build_start(Huaxue.t1, "st1"),
                             sql_build_start(Huaxue.t2, "st2"),
                             sql_build_start(Huaxue.t3, "st3"),
                             sql_build_start(Huaxue.t4, "st4"),
                             sql_build_start(Huaxue.t6, "st6"),
                             sql_build_start(Huaxue.t11, "st11"),
                             sql_build_start(Huaxue.t17, "st17"),
                             User.userName.label("updateUser"),
                             Huaxue.updateTime
                             ).outerjoin(User, Huaxue.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Huaxue.t1, Huaxue.t2, Huaxue.t3, Huaxue.t4, Huaxue.t5, Huaxue.t6, Huaxue.t7, Huaxue.t8, Huaxue.t9, Huaxue.t10, Huaxue.t11,
                   Huaxue.t12, Huaxue.t13, Huaxue.t14, Huaxue.t15, Huaxue.t16, Huaxue.t17, Huaxue.t18, Huaxue.t19, Huaxue.t20, Huaxue.t21,
                   func.JSON_LENGTH(Huaxue.i1).label("si1"), Huaxue.t22, Huaxue.t23,
                   User.userName.label("updateUser"), Huaxue.updateTime)
            .select_from(Huaxue)
            .outerjoin(User, Huaxue.userId == User.userId)
            .where(Huaxue.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Huaxue.i1).where(Huaxue.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: Huaxue, userId: int):
        # 检查图片是否存在
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                localPath = sub.img[len("/api/"):]
                if not await os.path.isfile(localPath):
                    raise FileNotFoundError(f"{sub.title} 图片不存在")
        # 读旧的i1
        old_i1_query = select(Huaxue.i1).where(Huaxue.subId == subId)
        old_i1: Optional[List[ImageTitle]] = await db.scalar(old_i1_query)
        # 新旧比较并做处理，如果不行，则类型出了问题
        await ImageTitle.edit_compare(db, item.i1, old_i1)
        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Huaxue).where(Huaxue.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        old_i1_query = select(Huaxue.i1).where(Huaxue.subId == subId)
        old_i1: Optional[List] = await db.scalar(old_i1_query)
        if old_i1 and len(old_i1) > 0:
            for old_sub in old_i1:
                localPath = old_sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    await async_os.remove(localPath)
        query = delete(Huaxue).where(Huaxue.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "5_化学成分"
        query = select(Huaxue).where(Huaxue.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                excel_data.append({
                    "序号": index,
                    "药材来源": ImageTitle.parse_html(record.t1),
                    "来源部位": ImageTitle.parse_html(record.t2),
                    "药材编号": ImageTitle.parse_html(record.t3),
                    "化合物名称": ImageTitle.parse_html(record.t4),
                    "化合物描述": ImageTitle.parse_html(record.t5),
                    "英文名称": ImageTitle.parse_html(record.t6),
                    "分子式": ImageTitle.parse_html(record.t7),
                    "分子量(g/mol)": ImageTitle.parse_html(record.t8),
                    "SMILES结构式": ImageTitle.parse_html(record.t9),
                    "理化性质": ImageTitle.parse_html(record.t10),
                    "化学结构分类": ImageTitle.parse_html(record.t11),
                    "紫外(UV)光谱": ImageTitle.parse_html(record.t12),
                    "红外(IR)光谱": ImageTitle.parse_html(record.t13),
                    "圆二色(CD)光谱": ImageTitle.parse_html(record.t14),
                    "核磁共振氢谱（1H NMR）": ImageTitle.parse_html(record.t15),
                    "核磁共振碳谱（13C NMR）": ImageTitle.parse_html(record.t16),
                    "提取方式": ImageTitle.parse_html(record.t17),
                    "含量范围（%或mg/g）": ImageTitle.parse_html(record.t18),
                    "含量变化因素": ImageTitle.parse_html(record.t19),
                    "药理活性描述": ImageTitle.parse_html(record.t20),
                    "作用靶点/通路": ImageTitle.parse_html(record.t21),
                    "分子结构图": f"{len(record.i1) if record.i1 else 0}张",
                    "文献/数据库来源": ImageTitle.parse_html(record.t22),
                    "备注说明": ImageTitle.parse_html(record.t23),
                })
                # 处理图片，批量复制多个文件到临时目录，并重新命名
                await ImageTitle.tcm_copy_file(record.i1, temp_dir, tcmName, subName, index)
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            return tcmName, subName, zip_buffer


class HuaxueReq(BaseModel):
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
    i1: Optional[List[ImageTitle]] = []

class HuaxueQueryParams(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t6: Optional[str] = None
    t11: Optional[str] = None
    t17: Optional[str] = None
