from sqlmodel import create_engine, SQLModel
from config import settings

from Database.ORM_Models.bag_models import BagInDB
from Database.ORM_Models.info_models import UserInDB, WorkerInDB
from Database.ORM_Models.transaction_models import UserPurchaseTransaction, CoinTransaction, BagScanTransaction


engine = create_engine(url=settings.database_url, echo=True)