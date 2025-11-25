from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.yaowu import YaowuReq, YaowuQueryParams, Yaowu
from app.models.user import User, get_curr_user
from app.utils.imgutil import ImageTitle

router = APIRouter(prefix="/api/yaowu", tags=["yaowu"])


@router.post("")
async def add(tcmId: int, item: YaowuReq, curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    await Yaowu.add(db, tcmId, item, curr_user.userId)
    return {"status": 0}


@router.get("/list")
async def get_list(tcmId: int, page: int = Query(1), perPage: int = Query(10), params: YaowuQueryParams = Depends(),
                   db: AsyncSession = Depends(get_db)):
    data = await Yaowu.get_list(db, tcmId, page, perPage, params)
    return {"status": 0, "data": data}


@router.get("")
async def get(subId: int, db: AsyncSession = Depends(get_db)):
    data = await Yaowu.get(db, subId)
    return {"status": 0, "data": data}


@router.put("")
async def edit(subId: int, item: YaowuReq, curr_user: User = Depends(get_curr_user),
               db: AsyncSession = Depends(get_db)):
    await Yaowu.edit(db, subId, item, curr_user.userId)
    return {"status": 0}


@router.delete("")
async def delete(subId: int, db: AsyncSession = Depends(get_db)):
    await Yaowu.delete(db, subId)
    return {"status": 0}


@router.get("/export")
async def export(tcmId: int, db: AsyncSession = Depends(get_db)):
    tcmName, subName, zip_file = await Yaowu.export(db, tcmId)
    return ImageTitle.resp_zip(tcmName, subName, zip_file)