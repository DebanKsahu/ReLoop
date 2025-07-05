from sqlmodel import Relationship, SQLModel, Field, Column, BigInteger, ForeignKey
from datetime import timezone, date, datetime
from Database.ORM_Models.info_models import UserInDB, WorkerInDB
from Utils.enums import ScanMode


class BagInDB(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(BigInteger,primary_key=True))
    user_id: int = Field(sa_column=Column(BigInteger,ForeignKey("userindb.id")))
    worker_id: int = Field(sa_column=Column(BigInteger,ForeignKey("workerindb.id")))
    number_of_time_used: int = Field(default=0)
    last_scan_date: date
    last_scan_type: ScanMode