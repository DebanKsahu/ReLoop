from fastapi import APIRouter

from Dashboard.user_dashboard import user_dashboard_router
from Dashboard.worker_dashboard import worker_dashboard_router

dashboard_router = APIRouter(prefix="/dashboard")

dashboard_router.include_router(user_dashboard_router)
dashboard_router.include_router(worker_dashboard_router)