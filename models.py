import datetime
from typing import Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr
from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(String)
    filename = Column(String)
    date_add = Column(Date)


    __table_args__ = {'schema': 'new_public'}


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(String)
    filename = Column(String)
    date_add = Column(Date)

    __table_args__ = {'schema': 'new_public'}


class Ad(BaseModel):
    title: str
    date_add: str
    description: list
    more: str


class MyUploadFile(BaseModel):
    filename: str
    content_type: str
    filetext: bytes = None

    @classmethod
    async def from_uploadfile(cls, upload_file: UploadFile):
        return cls(
            filename=upload_file.filename,
            content_type=upload_file.content_type,
            filetext=await upload_file.read()
        )


class ContactForm(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    message: str
    file: MyUploadFile = None


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    fullname = Column(String, nullable=True)

    __table_args__ = {'schema': 'new_public'}
