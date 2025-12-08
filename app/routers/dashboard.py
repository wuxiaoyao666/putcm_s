from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.bencao import Bencao, TcmType
from app.models.huaxue import Huaxue  # 确保导入 Huaxue 模型
from pydantic import BaseModel
from typing import List
import re

from app.models.kaifa import Kaifa
from app.models.yaoli import Yaoli

router = APIRouter(prefix="/api/data/dashboard", tags=["dashboard"])


class ChartItem(BaseModel):
    value: int
    name: str


class DashboardStats(BaseModel):
    bencao_type_count: List[ChartItem]
    huaxue_count: List[ChartItem]  # 第二个图表数据
    # ... 其他字段


"""去除HTML标签，提取纯文本"""


def strip_html(text: str) -> str:
    if not text:
        return "未填写"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()


@router.get("/stats")
async def get_dashboard_stats(response: Response, db: AsyncSession = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # --- 1. 收载品种 ---
    query_bencao = select(Bencao.tcmType, func.count(Bencao.subId)).group_by(Bencao.tcmType)
    res_bencao = await db.execute(query_bencao)
    bencao_data = []
    for t_type, count in res_bencao.all():
        type_name = TcmType.get(t_type, f"其他({t_type})")
        bencao_data.append(ChartItem(value=count, name=type_name))

    # --- 2. 收载化合物 ---
    query_huaxue = select(Huaxue.t5, func.count(Huaxue.subId)).group_by(Huaxue.t5)
    res_huaxue = await db.execute(query_huaxue)
    huaxue_data = []

    for t5_val, count in res_huaxue.all():
        name_clean = strip_html(str(t5_val)) if t5_val else "未分类"
        if not name_clean:
            name_clean = "未分类"

        huaxue_data.append(ChartItem(value=count, name=name_clean))

    # --- 3. 药理实验 ---
    query_yaoli = select(Yaoli.t5, func.count(Yaoli.subId)).group_by(Yaoli.t5)
    res_yaoli = await db.execute(query_yaoli)
    yaoli_data = []

    for t5_val, count in res_yaoli.all():
        name_clean = strip_html(str(t5_val)) if t5_val else "未分类"
        if not name_clean:
            name_clean = "未分类"

        yaoli_data.append(ChartItem(value=count, name=name_clean))

    # --- 4. 开发利用 ---
    query_kaifa = select(Kaifa.t3, func.count(Kaifa.subId)).group_by(Kaifa.t3)
    res_kaifa = await db.execute(query_kaifa)
    kaifa_data = []

    for t3_val, count in res_kaifa.all():
        name_clean = strip_html(str(t3_val)) if t3_val else "未分类"
        if not name_clean:
            name_clean = "未分类"

        kaifa_data.append(ChartItem(value=count, name=name_clean))

    return {
        "status": 0,
        "data": {
            "bencao_count": bencao_data,
            "huaxue_count": huaxue_data,
            "yaoli_count": yaoli_data,
            "kaifa_count": kaifa_data
        }
    }
