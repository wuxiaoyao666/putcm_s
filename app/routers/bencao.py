from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.database import get_db
from app.models.bencao import Bencao, BencaoReq
from app.models.user import User, get_curr_user
from app.utils.imgutil import ImageTitle

router = APIRouter(prefix="/api/bencao", tags=["bencao"])


@router.get("")
async def get(tcmId: int, db: AsyncSession = Depends(get_db)):
    data = await Bencao.get(db, tcmId)
    return {"status": 0, "data": data}


@router.put("")
async def edit(tcmId: int, item: BencaoReq, curr_user: User = Depends(get_curr_user),
               db: AsyncSession = Depends(get_db)):
    await Bencao.edit(db, tcmId, item, curr_user.userId)
    return {"status": 0}


@router.get("/export")
async def export(tcmId: int, db: AsyncSession = Depends(get_db)):
    tcmName, subName, zip_file = await Bencao.export(db, tcmId)
    return ImageTitle.resp_zip(tcmName, subName, zip_file)
