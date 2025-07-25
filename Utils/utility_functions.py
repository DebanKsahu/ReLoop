from typing import Any
from fastapi import UploadFile
from passlib.context import CryptContext
from pyzbar.pyzbar import decode
import numpy as np
import cv2
import jwt
from Utils.exceptions import HttpExceptions
from config import settings



class PasswordUtils():
    pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return PasswordUtils.pwdContext.verify(secret=plain_password,hash=hashed_password)
    
    @staticmethod
    def hash_password(plain_password: str):
        return PasswordUtils.pwdContext.hash(plain_password)
    
class JwtUtils():

    @staticmethod
    def create_jwt(data: dict[str,Any]):
        copied_data = data.copy()
        encoded_jwt = jwt.encode(copied_data,key=settings.secret_key,algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def decode_jwt(token: str) -> dict[str,Any]:
        payload: dict = jwt.decode(jwt=token,key=settings.secret_key,algorithms=[settings.algorithm])
        return payload
    
class ImageProcess():
    
    @staticmethod
    async def process_image(file: UploadFile):
        image_bytes = await file.read()
        np_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        decoded_objects = decode(img)
        if not decoded_objects:
            raise HttpExceptions.item_not_found("QR")
        if len(decoded_objects)>1 or len(decoded_objects)<=0:
            raise HttpExceptions.invalid_item("QR")
        raw_data = decoded_objects[0].data.decode('utf-8')

        return raw_data
