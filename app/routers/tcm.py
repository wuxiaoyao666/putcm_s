from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.tcm import Tcm, TcmReq
from app.models.tmpfile import TmpFile
from app.models.user import User, get_curr_user
from typing import List

router = APIRouter(prefix="/api/config/tcm", tags=["tcm"])


@router.post("/img")
async def up_img(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """预上传图片"""
    tcmImg = await TmpFile.add(db, file, "/tcm", "上传中药图片")
    return {"status": 0, "data": {"value": tcmImg}}


@router.post("")
async def add(item: TcmReq, curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    await Tcm.add(db, item, curr_user.userId)
    return {"status": 0, "msg": "添加成功"}


@router.get("/list")
async def get_list(page: int = 1, perPage: int = 10, db: AsyncSession = Depends(get_db)):
    data = await Tcm.get_list(db, page, perPage)
    return {"status": 0, "data": data}


@router.delete("")
async def del_by_tcmId(tcmId: int, db: AsyncSession = Depends(get_db)):
    await Tcm.del_by_tcmId(db, tcmId)
    return {"status": 0, "msg": "删除成功"}


@router.get("/recentlyview")
async def get_recentlyView(curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    # 根据用户，得到最近浏览的tcmId数组
    tcmIds: List[int] = curr_user.recentlyView
    if tcmIds and len(tcmIds) > 0:
        # 根据tcmId数组，查询tcm
        items = await Tcm.get_by_tcmIds(db, tcmIds)
        #建立tcmId到结果的映射（快速查找）
        res_map={item["tcmId"]:item for item in items}
        sort_items=[res_map.get(tcmId) for tcmId in tcmIds]
        #按照tcmIds排序
        return {"status": 0, "data": {
            "items": sort_items
        }}
    else:
        return {"status": 0, "data": []}


@router.get("/letterindex")
async def get_letterIndex(db: AsyncSession = Depends(get_db)):
    """得到界面结构，数据通过service二次传"""
    # 查询数据库，得到全部中药
    letters = await Tcm.get_letters(db)
    data = []
    for letter in letters:
        data.append({
            "type": "tpl", "tpl": letter, "className": "ml-28 text-lg text-red-800 font-bold"
        })
        data.append({
            "type": "service", "api": f"get:/api/config/tcm/letterindex/{letter}", "body": {
                "type": "cards", "columnCount": 4, "source": "$items", "className": "mt-5 ml-32", "card": {
                    "type": "container", "body": [{
                        "type": "image", "src": "$tcmImg", "thumbMode": "cover", "height": 200, "width": 150,
                        "className": "cursor-pointer", "onEvent": {
                            "click": {
                                "actions": [{
                                    "actionType": "ajax", "api": "put:/api/user/recentlyview?tcmId=$tcmId"
                                }, {
                                    "actionType": "link", "args": {
                                        "url": "/tcmall/bencao?tcmId=$tcmId&tcmName=$tcmName&menuName=本草考证"
                                    }
                                }]
                            }
                        }
                    }, {
                        "type": "flex", "items": {
                            "type": "tpl", "tpl": "$tcmName", "className": "text-red-800 font-bold"
                        }
                    }]
                }
            }})
    return {"status": 0, "data": data}


@router.get("/letterindex/{letter}")
async def get_letterIndex(letter: str, db: AsyncSession = Depends(get_db)):
    """根据字母查询所有数据"""
    items = await Tcm.get_by_letter(db, letter)
    return {"status": 0, "data": {"items": items}}
