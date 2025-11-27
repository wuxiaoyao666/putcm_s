import io
import os
import re
from typing import Dict

from fastapi import APIRouter, UploadFile, File, Depends
from openpyxl import  load_workbook
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app import User
from app.database import get_db
from app.models.gis import Gis
from app.models.tcm import Tcm
from app.models.user import get_curr_user

router = APIRouter(prefix="/api/gis", tags=["gis"])

# Excel 表头与数据库字段的映射关系
HEADER_MAPPING = {
    "药材名称": "tcmName",
    "样品类型": "sampleType",
    "采样类型": "samplingType",
    "样地编号": "plotNumber",
    "样品编号": "sampleNumber",
    "省份": "province",
    "城市": "city",
    "区县": "district",
    "乡镇": "township",
    "村庄": "village",
    "经度": "lng",
    "纬度": "lat",
    "海拔": "altitude",
    "采样人": "collector",
    "采样单位": "collectionUnit",
    "备注": "remarks"
}

@router.get("/template", summary="下载GIS导入模板")
async def download_template():
    # 文件的相对路径
    file_path = "file/template/gis.xlsx"

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return {"status": 1, "msg": "服务器端模板文件丢失，请联系管理员"}

    # 定义下载时的文件名
    download_filename = "GIS数据导入模板.xlsx"

    # 直接返回文件响应
    return FileResponse(
        path=file_path,
        filename=download_filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def clean_number(value):
    """清洗数值字符串"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    # 使用正则只保留数字和小数点
    str_val = str(value)
    # 提取数字部分
    match = re.search(r'-?\d+(\.\d+)?', str_val)
    if match:
        return float(match.group())
    return None


@router.post("/upload", summary="上传Excel导入GIS数据")
async def upload_excel(
        file: UploadFile = File(...),
        curr_user: User = Depends(get_curr_user),
        db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        return {"status": 1, "msg": "请上传 Excel 文件"}

    try:
        # 读取 Excel 文件
        contents = await file.read()
        wb = load_workbook(filename=io.BytesIO(contents), read_only=True, data_only=True)
        ws = wb.active

        # 获取表头并验证
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return {"status": 1, "msg": "文件内容为空"}

        headers = rows[0]
        header_map = {}

        for idx, header in enumerate(headers):
            if header in HEADER_MAPPING:
                header_map[idx] = HEADER_MAPPING[header]

        if "tcmName" not in header_map.values():
            return {"status": 1, "msg": "模板错误：缺少'药材名称'列"}

        # 预加载所有中药名称与ID的映射，避免循环查库
        tcm_query = select(Tcm.tcmName, Tcm.tcmId)
        tcm_res = await db.execute(tcm_query)
        tcm_map: Dict[str, int] = {name: tcm_id for name, tcm_id in tcm_res.all()}

        data_to_insert = []
        errors = []

        # 遍历数据行
        for row_idx, row in enumerate(rows[1:], start=2):
            row_data = {}
            tcm_name = None

            # 提取该行数据
            for col_idx, value in enumerate(row):
                if col_idx in header_map:
                    field_name = header_map[col_idx]

                    # 特殊处理字段
                    if field_name == "tcmName":
                        tcm_name = str(value).strip() if value else None
                        continue
                    else:
                        row_data[field_name] = str(value).strip() if value is not None else None

            # 数据校验
            if not tcm_name:
                continue

            if tcm_name not in tcm_map:
                errors.append(f"第{row_idx}行：药材'{tcm_name}'不存在，请先在系统中添加该药材")
                continue

            # 组装最终数据
            row_data["tcmId"] = tcm_map[tcm_name]
            data_to_insert.append(row_data)

        if errors:
            # 如果有错误，返回部分错误信息（限制数量避免太长）
            return {"status": 1, "msg": "导入失败", "errors": errors[:5]}

        if not data_to_insert:
            return {"status": 1, "msg": "没有有效数据可导入"}

        # 批量写入数据库
        await Gis.bulk_add(db, data_to_insert, curr_user.userId)

        return {"status": 0, "msg": f"成功导入 {len(data_to_insert)} 条数据"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": 1, "msg": f"处理文件时发生错误: {str(e)}"}


@router.get("/list")
async def get_list(tcmId: int, db: AsyncSession = Depends(get_db)):
    data = await Gis.get_list(db, tcmId)
    return {"status": 0, "data": data}