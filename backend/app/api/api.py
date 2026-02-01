from fastapi import APIRouter

from app.api.routes import projects, tasks, test, users

api_router = APIRouter()

api_router.include_router(test.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
