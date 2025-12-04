from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import Column, Integer, String, DECIMAL, Text, BigInteger, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base


class Gis(Base):
    __tablename__ = 'gis'

    subId = Column(Integer, primary_key=True, autoincrement=True)
    tcmId = Column(Integer, nullable=False, comment="关联tcm表的tcmId")

    # 分类与编号
    sampleType = Column(String(100), comment="样品类型")
    samplingType = Column(String(100), comment="采样类型")
    plotNumber = Column(String(100), comment="样地编号")
    sampleNumber = Column(String(100), comment="样品编号")

    # 地址信息
    province = Column(String(64))
    city = Column(String(64))
    district = Column(String(64))
    township = Column(String(100), comment="乡镇")
    village = Column(String(100), comment="村庄")

    # 坐标与环境
    lng = Column(DECIMAL(10, 6), comment="经度")
    lat = Column(DECIMAL(10, 6), comment="纬度")
    altitude = Column(DECIMAL(10, 2), comment="海拔")

    # 采样信息
    collector = Column(String(64), comment="采样人")
    collectionUnit = Column(String(100), comment="采样单位")
    remarks = Column(Text, comment="备注")

    # 系统字段
    userId = Column(Integer, comment="录入人")
    insertTime = Column(BigInteger)
    updateTime = Column(BigInteger)

    @staticmethod
    async def bulk_add(db: AsyncSession, data_list: List[Dict[str, Any]], userId: int):
        """批量添加GIS数据"""
        if not data_list:
            return

        now = int(datetime.now().timestamp())

        # 为每条数据注入系统字段
        for item in data_list:
            item['userId'] = userId
            item['insertTime'] = now
            item['updateTime'] = now

        stmt = insert(Gis).values(data_list)
        await db.execute(stmt)

    @staticmethod
    async def bulk_update(db: AsyncSession, data_list: List[Dict[str, Any]], userId: int):
        """批量更新GIS数据"""
        if not data_list:
            return

        now = int(datetime.now().timestamp())

        # 为每条数据注入更新时间和操作人
        for item in data_list:
            item['userId'] = userId
            item['updateTime'] = now
            # 注意：这里不要覆盖 insertTime

        # 使用 SQLAlchemy 的批量更新语法
        # data_list 中必须包含主键 'subId'，SQLAlchemy 会自动根据主键生成 WHERE subId = :subId
        await db.execute(update(Gis), data_list)

    @staticmethod
    async def get_list(db: AsyncSession, tcmId: int):
        """根据中药ID查询列表"""
        query = select(Gis).where(Gis.tcmId == tcmId)
        res = await db.execute(query)
        return res.scalars().all()