from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.tmpfile import TmpFile
from app.models.zhiwu import Zhiwu, ZhiwuReq, ZhiwuQueryParams
from app.models.user import User, get_curr_user
from app.utils.imgutil import ImageTitle

router = APIRouter(prefix="/api/zhiwu", tags=["zhiwu"])


@router.post("/img")
async def up_img(tcmId: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    img = await TmpFile.add(db, file, f"/{tcmId}", "上传原植物图片")
    return {"status": 0, "data": {"value": img}}


@router.post("")
async def add(tcmId: int, item: ZhiwuReq, curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    await Zhiwu.add(db, tcmId, item, curr_user.userId)
    return {"status": 0}


@router.get("/list")
async def get_list(tcmId: int, page: int = Query(1), perPage: int = Query(10), params: ZhiwuQueryParams = Depends(),
                   db: AsyncSession = Depends(get_db)):
    data = await Zhiwu.get_list(db, tcmId, page, perPage, params)
    return {"status": 0, "data": data}


@router.get("")
async def get(subId: int, db: AsyncSession = Depends(get_db)):
    data = await Zhiwu.get(db, subId)
    return {"status": 0, "data": data}


@router.get("/i1")
async def get(subId: int, db: AsyncSession = Depends(get_db)):
    data = await Zhiwu.get_i1(db, subId)
    return {"status": 0, "data": data}


@router.put("")
async def edit(subId: int, item: ZhiwuReq, curr_user: User = Depends(get_curr_user),
               db: AsyncSession = Depends(get_db)):
    await Zhiwu.edit(db, subId, item, curr_user.userId)
    return {"status": 0}


@router.delete("")
async def delete(subId: int, db: AsyncSession = Depends(get_db)):
    await Zhiwu.delete(db, subId)
    return {"status": 0}


@router.get("/export")
async def export(tcmId: int, db: AsyncSession = Depends(get_db)):
    tcmName, subName, zip_file = await Zhiwu.export(db, tcmId)
    return ImageTitle.resp_zip(tcmName, subName, zip_file)
