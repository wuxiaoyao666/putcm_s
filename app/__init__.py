from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database import AsyncSessionLocal
from app.models import User
from app.routers import auto_register_routers
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from app.utils.schutil import sch_clear_tmpfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    """定义生命周期上下文管理器，fastapi最新用法"""
    sch = AsyncIOScheduler()
    sch.add_job(sch_clear_tmpfile, 'interval', seconds=300)
    sch.start()
    logger.info("调度器已启动，定时任务60秒运行1次")

    app.state.sch = sch
    yield

    # 关闭时清理
    sch.shutdown()


logger.info("system start.")


def create_app() -> FastAPI:
    app = FastAPI(debug=True, title="test", docs_url=None, redoc_url=None, lifespan=lifespan)
    auto_register_routers(app)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                       allow_headers=["*"])

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,  # 关联项目的 OpenAPI 配置（默认 /openapi.json）
            title=app.title + " - Swagger UI",
            # 国内 CDN 的 Swagger CSS 文件（替换默认的 unpkg.com）
            swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui.css",
            # 国内 CDN 的 Swagger JS 文件
            swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui-bundle.js",
            # 国内 CDN 的 Swagger 初始化 JS 文件
            swagger_ui_parameters={
                "presets": [
                    "SwaggerUIBundle.presets.apis",
                    # 替换预设脚本为国内 CDN 地址
                    "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui-standalone-preset.js"
                ],
                "layout": "BaseLayout",  # 保持默认布局
            },
        )

    @app.middleware("http")
    async def user_token_handler(request: Request, call_next):
        # res = await call_next(request)
        # return res
        # 拦截器白名单
        if request.url.path.startswith("/api") and not request.url.path.startswith("/api/file") and not request.url.path.endswith("/export"):
            if request.url.path in ["/api/user/captcha", "/api/user/login"]:
                res = await call_next(request)
                return res
            authToken = request.headers.get("authToken")
            if authToken:
                async with AsyncSessionLocal() as db:
                    user = await User.get_bytoken(db, authToken)
                    if user:
                        request.state.user = user
                        try:
                            res = await call_next(request)
                            return res
                        except Exception as e:
                            logger.error(e)
                            return JSONResponse(status_code=200, content={"status": 1, "msg": str(e)})
                    else:
                        return JSONResponse(status_code=200, content={"status": 1, "msg": "登录token错误"})
            else:
                return JSONResponse(status_code=200, content={"status": 2, "msg": "登录token为空"})
        else:
            res = await call_next(request)
            return res

    return app
