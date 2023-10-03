from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr
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

class MyUploadFile(BaseModel):
    filename: str
    content_type: str
    filetext: bytes|None

    @classmethod
    async def from_uploadfile(cls, upload_file: UploadFile):
        return cls(
            filename= upload_file.filename,
            content_type= upload_file.content_type,
            filetext = await upload_file.read() if upload_file.filename else None
        )

class ContactForm(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    message: str
    file: MyUploadFile = None

