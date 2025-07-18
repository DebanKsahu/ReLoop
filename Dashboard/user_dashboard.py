from fastapi import APIRouter, Depends, HTTPException
from Database.ORM_Models.info_models import CoinInfo, UserInDB, UserProfileExpose
from Database.ORM_Models.response_models import SimpleResponse
from Database.ORM_Models.transaction_models import CoinTransaction, CoinTransactionExpose1, CoinTransactionExpose2, CoinTransactionShow
from Utils.dependency import oauth2_scheme, get_session
from Utils.enums import ResponseType, TransactionType
from Utils.router_classes import UserRouterClass
from Utils.utility_functions import JwtUtils
from sqlmodel import Session


user_dashboard_router = APIRouter(prefix="/user", tags=["Dashboard"], route_class=UserRouterClass)


@user_dashboard_router.get("/purchase_transactions")
def get_purchase_tarnsactions(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token)
    user_id = payload.get("id")
    user_info = session.get(UserInDB,user_id)
    if user_info is not None:
        return user_info.all_purchase_transaction
    
@user_dashboard_router.get("/coin_transactions")    
def coin_transactions(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token)
    user_id = payload.get("id",-1)
    user_info = session.get(UserInDB,user_id)
    if user_info is not None:
        type1_transactions = []
        type2_transactions = []
        for transaction in user_info.coin_transactions:
            if transaction.transaction_type==TransactionType.EARN:
                type2_transactions.append(CoinTransactionExpose2(**transaction.model_dump()))
            else:
                type1_transactions.append(CoinTransactionExpose1(**transaction.model_dump()))
        return CoinTransactionShow(spending_transactions=type1_transactions,earning_transactions=type2_transactions)
    
@user_dashboard_router.get("/coin_info")
def get_total_coin(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token)
    user_id = payload.get("id")
    user_info = session.get(UserInDB,user_id)
    if user_info is not None:
        coin_info = CoinInfo(
            current_coin_balance=user_info.current_coin_balance,
            total_coin_earned=user_info.total_coin_earned,
            total_coin_spend=user_info.total_coin_spend
        )
        return coin_info
    
@user_dashboard_router.get("/profile", response_model=UserProfileExpose)
def get_user_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token)
    user_id = payload.get("id")
    user_info = session.get(UserInDB,user_id)
    if user_info is not None:
        return user_info
    
@user_dashboard_router.post("/redeem/{coin_amount}")
def redeem_coin(coin_amount: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token)
    user_id = payload.get("id",-1)
    user_info = session.get(UserInDB,user_id)
    if user_info is not None:
        if coin_amount>user_info.current_coin_balance:
            raise HTTPException(status_code=400, detail="Not enough coins to complete the transaction.")
        elif coin_amount<=0:
            raise HTTPException(status_code=400, detail="Please enter a valid amount to complete the transaction.")
        else:
            new_transaction = CoinTransaction(
                user_id=user_id,
                bag_id=None,
                amount=coin_amount,
                transaction_type=TransactionType.SPEND
            )
            user_info.current_coin_balance = user_info.current_coin_balance-coin_amount
            user_info.total_coin_spend += coin_amount
            session.add(new_transaction)
            session.add(user_info)
            session.commit()
            return SimpleResponse(response_type=ResponseType.SUCCESS, message=f"{coin_amount} amount successfuly redeemed") 