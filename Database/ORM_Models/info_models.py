from typing import List
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, BigInteger
from Database.ORM_Models.transaction_models import BagScanTransaction, CoinTransaction, UserPurchaseTransaction

class UserInDB(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True, index=True))
    full_name: str 
    email: str = Field(unique=True, index=True)
    hashed_password: str

    total_beg_returned: int = Field(default=0, sa_column=Column(BigInteger))
    total_beg_collected: int = Field(default=0, sa_column=Column(BigInteger))
    current_coin_balance: int = Field(default=0, sa_column=Column(BigInteger))
    total_coin_earned: int = Field(default=0, sa_column=Column(BigInteger))
    total_coin_spend: int = Field(default=0,sa_column=Column(BigInteger))

    all_purchase_transaction: List[UserPurchaseTransaction] = Relationship(back_populates="user_info")
    all_bag_scans: List[BagScanTransaction] = Relationship(back_populates="user_info")
    coin_transactions: List[CoinTransaction] = Relationship()

class UserProfileExpose(SQLModel):
    id: int
    full_name: str
    email: str
    total_beg_returned: int
    total_beg_collected: int

class CoinInfo(SQLModel):
    current_coin_balance: int
    total_coin_earned: int 
    total_coin_spend: int 

class WorkerInDB(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True, index=True))
    full_name: str 
    email: str = Field(unique=True, index=True)
    hashed_password: str

    total_beg_scanned: int = Field(default=0, sa_column=Column(BigInteger))
    total_fault_scan: int = Field(default=0, sa_column=Column(BigInteger))

    all_bag_scans: List[BagScanTransaction] = Relationship(back_populates="worker_info")

class WorkerProfileExpose(SQLModel):
    id: int 
    full_name: str 
    email: str 
    total_beg_scanned: int 
    total_fault_scan: int 