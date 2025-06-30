from passlib.context import CryptContext
import jwt
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
    def create_jwt(data: dict):
        copied_data = data.copy()
        encoded_jwt = jwt.encode(copied_data,key=settings.secret_key,algorithm=settings.algorithm)
        return encoded_jwt