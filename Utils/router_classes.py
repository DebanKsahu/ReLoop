from typing import Any, Callable, Coroutine
from fastapi import Depends
from fastapi.routing import APIRoute
from sqlmodel import Session
from starlette.requests import Request
from starlette.responses import Response

from Database.Engine import engine
from Database.ORM_Models.info_models import UserInDB, WorkerInDB
from Utils.dependency import get_session
from Utils.exceptions import HttpExceptions
from Utils.utility_functions import JwtUtils

class UserRouterClass(APIRoute):
            
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_handler =  super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            auth_header = request.headers.get("Authorization")
            if auth_header is None:
                raise HttpExceptions.missing_token()
            elif not auth_header.startswith("Bearer "):
                raise HttpExceptions.invalid_token()
            token = auth_header.removeprefix("Bearer ").strip()
            if token == "":
                raise HttpExceptions.missing_token()
            payload = JwtUtils.decode_jwt(token)
            user_id = payload.get("id")
            if user_id is None:
                raise HttpExceptions.invalid_token()
            with Session(engine) as session:
                user_info = session.get(UserInDB, user_id)
                if user_info is None:
                    raise HttpExceptions.item_not_found("User")
            if user_info is None:
                raise HttpExceptions.item_not_found("User")
            response =  await original_handler(request)
            return response
        return custom_route_handler
    
class WorkerRouterClass(APIRoute):

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_handler =  super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            auth_header = request.headers.get("Authorization")
            if auth_header is None:
                raise HttpExceptions.missing_token()
            elif not auth_header.startswith("Bearer "):
                raise HttpExceptions.invalid_token()
            token = auth_header.removeprefix("Bearer ").strip()
            if token == "":
                raise HttpExceptions.missing_token()
            payload = JwtUtils.decode_jwt(token)
            worker_id = payload.get("id")
            if worker_id is None:
                raise HttpExceptions.invalid_token()
            with Session(engine) as session:
                user_info = session.get(WorkerInDB, worker_id)
                if user_info is None:
                    raise HttpExceptions.item_not_found("Worker")
            if user_info is None:
                raise HttpExceptions.item_not_found("Worker")
            response =  await original_handler(request)
            return response
        return custom_route_handler    