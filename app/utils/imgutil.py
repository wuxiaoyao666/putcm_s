from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from pydantic import BaseModel, Field
from typing import Optional, Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles.os as async_os
import os
import aiofiles
import pandas as pd
import io
import zipfile
from lxml import etree
from starlette.responses import StreamingResponse

from app.models.tmpfile import TmpFile


class ImageTitle(BaseModel):
    img: str
    title: str

    @staticmethod
    async def edit_compare(db: AsyncSession, new_i: Optional[List[ImageTitle]], old_i: Optional[List[ImageTitle]]):
        """新旧图片数据集比较，找出图片的不同；新有旧无删新临时记录；新无旧有，删旧文件；"""
        if new_i and len(new_i) > 0 and old_i and len(old_i) > 0:  # 新旧都有，进行逐项比较
            # 把旧的转换成img数组
            old_imgs = [old_sub.get("img") for old_sub in old_i]
            for new_sub in new_i:
                if new_sub.img not in old_imgs:  # 新有旧无
                    await TmpFile.delRecord(db, new_sub.img)
                else:  # 新有旧有,旧的数组删除
                    old_imgs.remove(new_sub.img)
            # old还有剩余，则删旧文件
            if len(old_imgs) > 0:
                for old_img in old_imgs:
                    localPath = old_img[len("/api/"):]
                    if Path(localPath).exists():
                        await async_os.remove(localPath)
        elif new_i and len(new_i) > 0 and (not old_i or len(old_i) == 0):  # 新有旧无，删临时记录
            for new_sub in new_i:
                await TmpFile.delRecord(db, new_sub.img)
        elif (not new_i or len(new_i) == 0) and old_i and len(old_i) > 0:  # 新无旧有，删文件
            for old_sub in old_i:
                localPath = old_sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    await async_os.remove(localPath)
        else:  # 新无旧无
            pass

    @staticmethod
    async def tcm_copy_file(field, temp_dir: str, tcmName: str, subName: str, index: int):
        if field and len(field) > 0:
            j = 1
            for sub in field:
                localPath = sub.get("img")[len("/api/"):]
                if Path(localPath).exists():
                    ext = Path(localPath).suffix
                    title = sub.get('title') or ""
                    safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_")
                    new_path = os.path.join(temp_dir, f"{tcmName}_{subName}_{index}.{j}_{safe_title}{ext}")
                    async with aiofiles.open(localPath, "rb") as src_file:
                        async with aiofiles.open(new_path, "wb") as dst_file:
                            while True:
                                chunk = await src_file.read(1014 * 1014)
                                if not chunk:
                                    break
                                await dst_file.write(chunk)
                j = j + 1

    @staticmethod
    async def export_zip(temp_dir: str, tcmName: str, subName: str, excel_data: List) -> io.BytesIO:
        # 生成excel文件
        excel_filename = os.path.join(temp_dir, f"{tcmName}_{subName}.xlsx")
        df = pd.DataFrame(excel_data)
        with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="数据")
        # 压缩zip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                zipf.write(file_path, file)
        # 重置zip文件指针
        zip_buffer.seek(0)
        return zip_buffer

    @staticmethod
    def parse_html(html: str) -> str:
        if not html:
            return ""
        tree = etree.HTML(html)
        text_nodes = tree.xpath("//text()")
        # 过滤空字符串，拼接非空文本（用空格分隔避免内容粘连）
        plain_text = ' '.join([text.strip() for text in text_nodes if text.strip()])
        return plain_text

    @staticmethod
    def resp_zip(tcmName:str, subName:str, zip_file: io.BytesIO):
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = quote(f"{tcmName}_{subName}_{timestamp}.zip")

        # 返回zip文件
        return StreamingResponse(zip_file, media_type="application/zip",
                                 headers={
                                     "Content-Disposition": f"attachment; filename*=UTF-8''{filename}; filename={filename};"
                                 })
