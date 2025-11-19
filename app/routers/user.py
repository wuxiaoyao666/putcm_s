from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from starlette.responses import StreamingResponse
from datetime import datetime

from ..database import get_db
from ..extensions import snowflake
from ..models import User
import sqlalchemy
from loguru import logger

from ..models.imgcaptcha import ImgCaptcha
from ..models.user import LoginReq, get_curr_user
from ..utils.loginutil import generate_captcha

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/hello")
async def hello():
    logger.info(f"hello")
    return {"hello": "world"}


@router.get("/count")
async def get_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count()).select_from(User))
    count = result.scalar()
    return {"count": count}


@router.post("/login")
async def login(user: LoginReq, db: AsyncSession = Depends(get_db)):
    # 1.查询验证码
    captcha_res = await ImgCaptcha.check_captcha(db, user.captcha)
    # 2.查询用户名和密码
    userpwd_res = await User.login_check(db, user.username, user.password)
    if not captcha_res:
        return {"status": 1, "msg": "验证码无效"}
    if not userpwd_res:
        return {"status": 2, "msg": "用户名或密码错误"}
    # 3.删除本验证码
    await ImgCaptcha.del_by_captchaText(db, user.captcha)
    # 4.生成登录token
    authToken = str(next(snowflake))
    # 5.保存token
    await User.update_token(db, user.username, user.password, authToken)
    return {"status": 0, "data": {"token": authToken}}


@router.get("/captcha", summary="生成数字验证码图片")
async def gen_captcha(db: AsyncSession = Depends(get_db)):
    img, text = generate_captcha()
    # 1.删除超时验证码
    await ImgCaptcha.del_all_expire(db)
    # 2.保存到数据库
    await ImgCaptcha.add(db, text)
    return StreamingResponse(content=img,
                             media_type="image/png",
                             headers={
                                 "Captcha-Length": "4",
                                 "Cache-Control": "no-cache,no-store,must-revalidate",
                                 "Pragma": "no-cache",
                                 "Expires": "0"
                             })


@router.get("/info")
async def get_info(curr_user: User = Depends(get_curr_user)):
    return {"status": 0, "data": {
        "userName": curr_user.userName,
        "userRole": curr_user.userRole,
    }}


@router.put("/recentlyview")
async def view_tcm(tcmId: int, curr_user: User = Depends(get_curr_user), db: AsyncSession = Depends(get_db)):
    """用户点击某中药，后台记录 最近浏览"""
    # 读当前 最近浏览
    tcmIds: List[int] = curr_user.recentlyView
    # 如果为空，则初始化为[]
    if not tcmIds:
        tcmIds = []
    # 如果存在，则删除当前tcmId
    if tcmId in tcmIds:
        tcmIds.remove(tcmId)
    # 加入数组
    tcmIds.insert(0, tcmId)
    # 超长删除
    if len(tcmIds) > 10:
        tcmIds = tcmIds[:10]
    # 更新到表
    await User.update_recentlyview(db, curr_user.userId, tcmIds)
    return {"status": 0, "msg": ""}