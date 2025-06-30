from sqlmodel import create_engine, SQLModel
from config import settings


engine = create_engine(url=settings.database_url, echo=True)