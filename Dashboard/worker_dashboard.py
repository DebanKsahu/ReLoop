from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, Form, UploadFile
from Database.ORM_Models.bag_models import BagInDB
from Database.ORM_Models.info_models import UserInDB, WorkerInDB, WorkerProfileExpose
from Database.ORM_Models.response_models import SimpleResponse
from Database.ORM_Models.transaction_models import BagScanTransaction, BagScanTransactionExpose, CoinTransaction, UserPurchaseTransaction
from Utils.dependency import oauth2_scheme, get_session
from Utils.enums import ResponseType, ScanMode, TransactionType
from Utils.exceptions import HttpExceptions
from Utils.router_classes import WorkerRouterClass
from Utils.utility_functions import ImageProcess, JwtUtils
from sqlmodel import Session

worker_dashboard_router = APIRouter(prefix="/worker", tags=["Dashboard"], route_class=WorkerRouterClass)

@worker_dashboard_router.get("/scan_transactions")
def get_scan_transactions(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token=token)
    worker_id = payload.get("id")
    worker_info = session.get(WorkerInDB,worker_id)
    if worker_info is not None:
        all_scans = list(worker_info.all_bag_scans)
        result: List[BagScanTransactionExpose] = []
        for index,scan in enumerate(all_scans):
            result.append(BagScanTransactionExpose(**scan.model_dump()))
        return result
    
@worker_dashboard_router.get("/profile",response_model=WorkerProfileExpose)
def get_profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token=token)
    worker_id = payload.get("id")
    worker_info = session.get(WorkerInDB,worker_id)
    if worker_info is not None:
        return worker_info
    
@worker_dashboard_router.post("/scan_qr")
async def scan_qr(uploaded_qr: UploadFile, scan_mode: ScanMode = Form(), user_id: int = Form(), token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token=token)
    worker_id = payload.get("id",-1)
    worker_info = session.get(WorkerInDB,worker_id)
    user_info = session.get(UserInDB,user_id)
    if user_info is None:
        raise HttpExceptions.item_not_found("User")
    if worker_info is not None:
        qr_data = await ImageProcess.process_image(uploaded_qr)
        qr_data = int(qr_data)
        if scan_mode==ScanMode.CHECKOUT:
            old_bag = session.get(BagInDB,qr_data)
            if old_bag is None:
                new_bag=BagInDB(id=qr_data,user_id=user_id,worker_id=worker_id,last_scan_date=datetime.now(timezone.utc).date(),last_scan_type=ScanMode.CHECKOUT,number_of_time_used=1)
                session.add(new_bag)
            else:
                old_bag.user_id = user_id
                old_bag.worker_id = worker_id
                old_bag.last_scan_date = datetime.now(timezone.utc).date()
                old_bag.last_scan_type = ScanMode.CHECKOUT
                old_bag.number_of_time_used = old_bag.number_of_time_used + 1
                session.add(old_bag)
            new_scan_transaction = BagScanTransaction(
                bag_id=qr_data,
                user_id=user_id,
                worker_id=worker_id,
                scan_mode=ScanMode.CHECKOUT
            )
            new_purchase_transaction = UserPurchaseTransaction(
                user_id=user_id,
                bag_used=1
            )
            user_info.total_beg_collected = user_info.total_beg_collected+1
            worker_info.total_beg_scanned = worker_info.total_beg_scanned+1
            session.add(new_scan_transaction)
            session.add(new_purchase_transaction)
            session.add(user_info)
            session.add(worker_info)
        else:
            old_bag = session.get(BagInDB,qr_data)
            if old_bag is None:
                raise HttpExceptions.invalid_item("Bag")
            else:
                old_bag.user_id = user_id
                old_bag.worker_id = worker_id
                old_bag.last_scan_date = datetime.now(timezone.utc).date()
                old_bag.last_scan_type = ScanMode.RECYCLE
                session.add(old_bag)
            new_scan_transaction = BagScanTransaction(
                bag_id=qr_data,
                user_id=user_id,
                worker_id=worker_id,
                scan_mode=ScanMode.RECYCLE
            )
            new_coin_transaction = CoinTransaction(
                user_id=user_id,
                bag_id=qr_data,
                amount=30-old_bag.number_of_time_used,
                transaction_type=TransactionType.EARN
            )
            user_info.total_beg_returned = user_info.total_beg_returned+1
            user_info.current_coin_balance = user_info.current_coin_balance+30-old_bag.number_of_time_used
            user_info.total_coin_earned = user_info.total_coin_earned+30-old_bag.number_of_time_used
            worker_info.total_beg_scanned = worker_info.total_beg_scanned+1
            session.add(old_bag)
            session.add(new_coin_transaction)
            session.add(new_scan_transaction)
            session.add(user_info)
            session.add(worker_info)
        session.commit()
        return SimpleResponse(response_type=ResponseType.SUCCESS,message="Scan successfully completed")

@worker_dashboard_router.post("/about_bag")
async def get_bag_info(uploaded_qr: UploadFile, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = JwtUtils.decode_jwt(token=token)
    worker_id = payload.get("id",-1)
    worker_info = session.get(WorkerInDB,worker_id)
    if worker_info is not None:
        qr_data = await ImageProcess.process_image(uploaded_qr)
        qr_data = int(qr_data)
        bag_info = session.get(BagInDB,qr_data)
        if bag_info is None:
            raise HttpExceptions.item_not_found("Bag with this QR")
        else:
            return bag_info