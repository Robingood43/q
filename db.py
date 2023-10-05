from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv


load_dotenv()
engine = create_async_engine(url=os.getenv('DATABASE_URL'), echo = True)


class Base(DeclarativeBase):
    pass