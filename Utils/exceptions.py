from fastapi import HTTPException, status


class HttpExceptions():

    @staticmethod
    def item_not_found(item_name: str):
        return HTTPException(status_code=404, detail=f"{item_name} not found")
    
    @staticmethod
    def wrong_authentication():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @staticmethod
    def item_already_exist(item_name: str):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{item_name} already exists."
        )
    
    @staticmethod
    def invalid_item(item_name: str):
        return HTTPException(status_code=400, detail=f"{item_name} is invalid")
    
    @staticmethod
    def missing_token():
        return HTTPException(status_code=401, detail="Missing token")
    
    @staticmethod
    def invalid_token():
        return HTTPException(status_code=401, detail="Invalid token")
    