from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, PrimaryKeyConstraint

class UserInDB(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True, index=True))
    full_name: str 
    email: str = Field(unique=True, index=True)
    hashed_password: str

    total_beg_returned: int = Field(default=0, sa_column=Column(BigInteger))
    total_beg_collected: int = Field(default=0, sa_column=Column(BigInteger))

class WorkerInDB(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True, index=True))
    full_name: str 
    email: str = Field(unique=True, index=True)
    hashed_password: str

    total_beg_scanned: int = Field(default=0, sa_column=Column(BigInteger))
    total_fault_scan: int = Field(default=0, sa_column=Column(BigInteger))