import importlib
from fastapi import FastAPI
import pkgutil

def auto_register_routers(app:FastAPI):
    # 自动发现并注册所有蓝图
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f'.{module_name}', __name__)
        if hasattr(module, 'router'):
            app.include_router(module.router)
