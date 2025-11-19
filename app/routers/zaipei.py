from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.database import get_db
from app.models.tmpfile import TmpFile
from app.models.zaipei import Zaipei, ZaipeiReq, ZaipeiQueryParams
from app.models.user import User, get_curr_user
from app.utils.imgutil import ImageTitle

router = APIRouter(prefix="/api/zaipei", tags=["zaipei"])


@router.post("")
async def add(tcmId: int, item: ZaipeiReq, curr_user: User = Depends(get_curr_user),
              db: AsyncSession = Depends(get_db)):
    await Zaipei.add(db, tcmId, item, curr_user.userId)
    return {"status": 0}


@router.get("/list")
async def get_list(tcmId: int, page: int = Query(1), perPage: int = Query(10), params: ZaipeiQueryParams = Depends(),
                   db: AsyncSession = Depends(get_db)):
    data = await Zaipei.get_list(db, tcmId, page, perPage, params)
    return {"status": 0, "data": data}


@router.get("")
async def get(subId: int, db: AsyncSession = Depends(get_db)):
    data = await Zaipei.get(db, subId)
    return {"status": 0, "data": data}


@router.put("")
async def edit(subId: int, item: ZaipeiReq, curr_user: User = Depends(get_curr_user),
               db: AsyncSession = Depends(get_db)):
    await Zaipei.edit(db, subId, item, curr_user.userId)
    return {"status": 0}


@router.delete("")
async def delete(subId: int, db: AsyncSession = Depends(get_db)):
    await Zaipei.delete(db, subId)
    return {"status": 0}


@router.get("/export")
async def export(tcmId: int, db: AsyncSession = Depends(get_db)):
    tcmName, subName, zip_file = await Zaipei.export(db, tcmId)
    return ImageTitle.resp_zip(tcmName, subName, zip_file)
