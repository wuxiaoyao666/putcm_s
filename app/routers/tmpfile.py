from aiofiles import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/file", tags=["file"])


@router.get("/{file_path:path}")
async def get_file(file_path: str):
    """获取多级文件路径"""
    all_path = f"file/{file_path}"
    if not await os.path.isfile(all_path):
        return {"status": 1, "msg": "文件不存在"}
    else:
        return FileResponse(all_path)
