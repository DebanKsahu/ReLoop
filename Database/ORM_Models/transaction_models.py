import datetime
from typing import List, Self
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, BigInteger, ForeignKey
from datetime import date, timezone, datetime
from Utils.enums import ScanMode, TransactionType
from pydantic import model_validator

class UserPurchaseTransaction(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True)) 
    user_id: int = Field(sa_column=Column(BigInteger, ForeignKey("userindb.id")))
    bag_used: int = Field(default=0)
    transaction_date: date = Field(default_factory=lambda : datetime.now(timezone.utc).date())

    user_info: "UserInDB" = Relationship(back_populates="all_purchase_transaction") # type: ignore

class CoinTransaction(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True)) 
    user_id: int = Field(sa_column=Column(BigInteger, ForeignKey("userindb.id")))
    bag_id: int | None
    transaction_date: date = Field(default_factory=lambda : datetime.now(timezone.utc).date())
    amount: int = Field(sa_column=Column(BigInteger))
    transaction_type: TransactionType

    @model_validator(mode="after")
    def validate_tx_type(self) -> Self:
        if self.bag_id==None and self.transaction_type==TransactionType.EARN:
            raise ValueError("Invalid object creation. bag_id is None")
        elif self.bag_id!=None and self.transaction_date==TransactionType.SPEND:
            raise ValueError("Invalid object creation. transaction_type must be TransactionType.EARN")
        return self
    
class CoinTransactionExpose1(SQLModel):
    id: int 
    user_id: int 
    transaction_date: date 
    amount: int 

class CoinTransactionExpose2(SQLModel):
    id: int 
    user_id: int 
    bag_id: int
    transaction_date: date 
    amount: int 

class CoinTransactionShow(SQLModel):
    type1: List[CoinTransactionExpose1]
    type2: List[CoinTransactionExpose2]
    
class BagScanTransaction(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True))
    bag_id: int = Field(sa_column=Column(BigInteger, ForeignKey("bagindb.id")))
    user_id: int = Field(sa_column=Column(BigInteger,ForeignKey("userindb.id")))
    worker_id: int = Field(sa_column=Column(BigInteger,ForeignKey("workerindb.id")))
    scan_date: date = Field(default_factory=lambda : datetime.now(timezone.utc).date())
    scan_mode: ScanMode

    user_info: "UserInDB" = Relationship(back_populates="all_bag_scans") # type: ignore
    worker_info: "WorkerInDB" = Relationship(back_populates="all_bag_scans") # type: ignore

class BagScanTransactionExpose(SQLModel):
    id: int
    bag_id: int
    scan_mode: ScanMode
    scan_date: date