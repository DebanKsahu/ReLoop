from fastapi import APIRouter, Depends
import jwt
from sqlmodel import Session, select
from Utils.dependency import get_session
from Database.ORM_Models.auth_models import UserLogin, UserSignup, WorkerLogin, WorkerSignup
from Database.ORM_Models.info_models import UserInDB, WorkerInDB
from Database.ORM_Models.token_models import Token
from Database.ORM_Models.response_models import SimpleResponse, ResponseType
from Utils.exceptions import HttpExceptions
from Utils.utility_functions import PasswordUtils, JwtUtils
from Utils.enums import LoggerType

auth_router = APIRouter(prefix="/auth",tags=["Authentication"])

@auth_router.post("/user/signup", response_model=SimpleResponse)
def user_signup(signup_data: UserSignup, session: Session = Depends(get_session)):
    user_info = session.exec(select(UserInDB).where(UserInDB.email==signup_data.email)).first()
    if user_info is not None:
        raise HttpExceptions.item_already_exist(item_name="User Email")
    new_user_info = UserInDB(
        full_name=signup_data.full_name,
        email=signup_data.email,
        hashed_password=PasswordUtils.hash_password(signup_data.password)
    )

    session.add(new_user_info)
    session.commit()
    return SimpleResponse(response_type=ResponseType.SUCCESS, message="Account Successfuly Created")

@auth_router.post("/user/login", response_model=Token)
def user_login(login_data: UserLogin, session: Session = Depends(get_session)):
    user_info = session.exec(select(UserInDB).where(UserInDB.email==login_data.email)).first()
    if user_info is None:
        raise HttpExceptions.item_not_found("Email")
    if PasswordUtils.verify_password(plain_password=login_data.password, hashed_password=user_info.hashed_password) is False:
        raise HttpExceptions.wrong_authentication()
    jwt_payload = {"id": user_info.id, "logger_type": LoggerType.USER}
    access_token = JwtUtils.create_jwt(jwt_payload)
    return Token(access_token=access_token,token_type="bearer")

@auth_router.post("/worker/signup", response_model=SimpleResponse)
def worker_signup(signup_data: WorkerSignup, session: Session = Depends(get_session)):
    worker_info = session.get(WorkerInDB,signup_data.email)
    if worker_info is not None:
        raise HttpExceptions.item_already_exist(item_name="Worker Email")
    new_worker_info = WorkerInDB(
        full_name=signup_data.full_name,
        email=signup_data.email,
        hashed_password=PasswordUtils.hash_password(signup_data.password)
    )

    session.add(new_worker_info)
    session.commit()
    return SimpleResponse(response_type=ResponseType.SUCCESS, message="Account Successfuly Created")

@auth_router.post("/worker/login", response_model=Token)
def worker_login(login_data: WorkerLogin, session: Session = Depends(get_session)):
    worker_info = session.get(WorkerInDB,login_data.worker_id)
    if worker_info is None:
        raise HttpExceptions.item_not_found("Worker Id")
    if PasswordUtils.verify_password(plain_password=login_data.password, hashed_password=worker_info.hashed_password) is False:
        raise HttpExceptions.wrong_authentication()
    jwt_payload = {"id": worker_info.id, "logger_type": LoggerType.WORKER}
    access_token = JwtUtils.create_jwt(jwt_payload)
    return Token(access_token=access_token,token_type="bearer")
