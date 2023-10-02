from pydantic import BaseModel
from db import Base
from sqlalchemy import Column, Integer, String

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(String)
    filename = Column(String)
    date = Column(String)
    __table_args__ = {'schema': 'new_public'}

class Ad(BaseModel):
    title: str
    date:str
    description: str
