from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.yaoli import Yaoli, YaoliReq, YaoliQueryParams

from app.models.user import User, get_curr_user
from app.utils.imgutil import ImageTitle

router = APIRouter(prefix="/api/yaoli", tags=["yaoli"])


@router.post("")
async def add(tcmId: int, item: YaoliReq, curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    await Yaoli.add(db, tcmId, item, curr_user.userId)
    return {"status": 0}


@router.get("/list")
async def get_list(tcmId: int, page: int = Query(1), perPage: int = Query(10), params: YaoliQueryParams = Depends(),
                   db: AsyncSession = Depends(get_db)):
    data = await Yaoli.get_list(db, tcmId, page, perPage, params)
    return {"status": 0, "data": data}


@router.get("")
async def get(subId: int, db: AsyncSession = Depends(get_db)):
    data = await Yaoli.get(db, subId)
    return {"status": 0, "data": data}


@router.put("")
async def edit(subId: int, item: YaoliReq, curr_user: User = Depends(get_curr_user),
               db: AsyncSession = Depends(get_db)):
    await Yaoli.edit(db, subId, item, curr_user.userId)
    return {"status": 0}


@router.delete("")
async def delete(subId: int, db: AsyncSession = Depends(get_db)):
    await Yaoli.delete(db, subId)
    return {"status": 0}


@router.get("/export")
async def export(tcmId: int, db: AsyncSession = Depends(get_db)):
    tcmName, subName, zip_file = await Yaoli.export(db, tcmId)
    return ImageTitle.resp_zip(tcmName, subName, zip_file)