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


class Zhiwu(Base):
    __tablename__ = "zhiwu"
    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, comment="中药ID")
    t1 = Column(TEXT, comment="药材基源")
    t2 = Column(TEXT, comment="形态描述")
    i1 = Column(JSON, comment="形态图片（list，{img,title}")
    t3 = Column(TEXT, comment="自然分布区")
    t4 = Column(TEXT, comment="养殖种植区域")
    t5 = Column(TEXT, comment="来源典籍文献")
    t6 = Column(TEXT, comment="备注")
    userId = Column(Integer, comment="数据录入人ID")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def add(db: AsyncSession, tcmId: int, item: ZhiwuReq, userId: int):
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
        query = insert(Zhiwu).values(**values)
        await db.execute(query)
        await db.commit()
        # 删除临时文件记录
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                await TmpFile.delRecord(db, sub.img)

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int, page: int, perPage: int, params: ZhiwuQueryParams):
        # 公共查询条件
        def base_query(s: Select):
            query = s.where(Zhiwu.tcmId == tcmId)
            for field, value in params.model_dump(exclude_none=True).items():
                query = query.where(getattr(Zhiwu, field).like(f"%{value}%"))
            return query

        # 查询总个数
        total_query = base_query(select(func.count()))
        total = await db.scalar(total_query)

        # 计算偏移量
        offset = (page - 1) * perPage
        items_query = select(Zhiwu.subId,
                             sql_build_start(Zhiwu.t1, "st1"),
                             sql_build_start(Zhiwu.t2, "st2"),
                             func.JSON_LENGTH(Zhiwu.i1).label("si1"),
                             sql_build_start(Zhiwu.t3, "st3"),
                             sql_build_start(Zhiwu.t4, "st4"),
                             sql_build_start(Zhiwu.t5, "st5"),
                             User.userName.label("updateUser"),
                             Zhiwu.updateTime
                             ).outerjoin(User, Zhiwu.userId == User.userId)
        items_res = await db.execute(base_query(items_query).offset(offset).limit(perPage))
        items = items_res.mappings().all()
        return {"total": total, "items": items}

    @staticmethod
    async def get(db: AsyncSession, subId: int):
        query = (
            select(Zhiwu.t1, Zhiwu.t2, Zhiwu.i1, func.JSON_LENGTH(Zhiwu.i1).label("si1"), Zhiwu.t3, Zhiwu.t4, Zhiwu.t5,
                   Zhiwu.t6, User.userName.label("updateUser"), Zhiwu.updateTime)
            .select_from(Zhiwu)
            .outerjoin(User, Zhiwu.userId == User.userId)
            .where(Zhiwu.subId == subId))
        res = await db.execute(query)
        item = res.mappings().one_or_none()
        return item

    @staticmethod
    async def get_i1(db: AsyncSession, subId: int):
        query = select(Zhiwu.i1).where(Zhiwu.subId == subId)
        data = await db.scalar(query)
        return data

    @staticmethod
    async def edit(db: AsyncSession, subId: int, item: ZhiwuReq, userId: int):
        # 检查图片是否存在
        if item.i1 and len(item.i1) > 0:
            for sub in item.i1:
                localPath = sub.img[len("/api/"):]
                if not await os.path.isfile(localPath):
                    raise FileNotFoundError(f"{sub.title} 图片不存在")
        # 读旧的i1
        old_i1_query = select(Zhiwu.i1).where(Zhiwu.subId == subId)
        old_i1: Optional[List[ImageTitle]] = await db.scalar(old_i1_query)
        # 新旧比较并做处理，如果不行，则类型出了问题
        await ImageTitle.edit_compare(db, item.i1, old_i1)
        # 转换为有效dict,不能过滤掉空值，因为空值有意义
        values = item.model_dump()
        values['userId'] = userId
        now = int(datetime.now().timestamp())
        values["updateTime"] = now
        query = update(Zhiwu).where(Zhiwu.subId == subId).values(values)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, subId: int):
        old_i1_query = select(Zhiwu.i1).where(Zhiwu.subId == subId)
        old_i1: Optional[List] = await db.scalar(old_i1_query)
        if old_i1 and len(old_i1) > 0:
            for old_sub in old_i1:
                localPath = old_sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    await async_os.remove(localPath)
        query = delete(Zhiwu).where(Zhiwu.subId == subId)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def export(db: AsyncSession, tcmId: int) -> Tuple[str, str, io.BytesIO]:
        tcmName = await Tcm.get_tcmName(db, tcmId)
        subName = "2_原植物（动物）"
        query = select(Zhiwu).where(Zhiwu.tcmId == tcmId)
        res = await db.execute(query)
        records = res.scalars().all()

        with tempfile.TemporaryDirectory() as temp_dir:
            excel_data = []
            index = 1
            for record in records:
                # 处理文本字段
                excel_data.append({
                    "序号": index,
                    "药材基原": ImageTitle.parse_html(record.t1),
                    "形态描述": ImageTitle.parse_html(record.t2),
                    "形态图片": f"{len(record.i1) if record.i1 else 0}张",
                    "自然分布区": ImageTitle.parse_html(record.t3),
                    "养殖、种植区域": ImageTitle.parse_html(record.t4),
                    "来源典籍/文献": ImageTitle.parse_html(record.t5),
                    "备注": ImageTitle.parse_html(record.t6)
                })
                # 处理图片，批量复制多个文件到临时目录，并重新命名
                await ImageTitle.tcm_copy_file(record.i1, temp_dir, tcmName, subName, index)
                index += 1
            zip_buffer = await ImageTitle.export_zip(temp_dir, tcmName, subName, excel_data)
            # # 保存到本地（自定义本地路径和文件名）
            # local_zip_path = f"1.zip"  # 可修改路径，如 "./exports/xxx.zip"
            # with open(local_zip_path, "wb") as f:
            #     f.write(zip_buffer.getvalue())  # 读取缓冲区所有二进制数据写入本地文件
            #
            # # 关键步骤2：再次重置指针（供StreamingResponse返回给浏览器）
            # zip_buffer.seek(0)
            return tcmName, subName, zip_buffer


class ZhiwuReq(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
    t6: Optional[str] = None
    i1: Optional[List[ImageTitle]] = []


class ZhiwuQueryParams(BaseModel):
    t1: Optional[str] = None
    t2: Optional[str] = None
    t3: Optional[str] = None
    t4: Optional[str] = None
    t5: Optional[str] = None
