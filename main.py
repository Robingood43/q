import os
import glob
import aiosmtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
from starlette.templating import Jinja2Templates
import datetime
from db import engine
from crud import Crud
from models import Ad, Document, ContactForm, MyUploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker


app = FastAPI()
app.mount("/static/image", StaticFiles(directory="static/image"), name="static")
templates = Jinja2Templates(directory="templates")
session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = Crud()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ads = [Ad(title="Ad 1",date = '06.11.2022', description="This is a description for Ad 1."),
           Ad(title="Ad 2",date = '08.10.2022', description="This is a description for Ad 2.")]
    return templates.TemplateResponse("index.html", {"request": request, "ads": ads})


@app.get("/documents/{document_name}", response_class=HTMLResponse)
async def download_document(document_name):
    return FileResponse(path="static/documents/"+document_name)


@app.get("/documents.html", response_class=HTMLResponse)
async def get_documents(request: Request):
    all_data = await db.get_all(session)
    all_docs_db = {i.filename for i in all_data}
    all_docs_path = {os.path.basename(i) for i in glob.glob("static/documents/*")}
    docs_add = all_docs_path.difference(all_docs_db)
    docs_delete = all_docs_db.difference(all_docs_path)

    if docs_add:
        new_docs = [Document(size = f"{(os.path.getsize('static/documents/'+filename) / 1024):.2f}",
                            filename = filename,
                            date = f"{datetime.datetime.now().strftime('%d.%m.%Y')}")for filename in docs_add]
        await db.add(session, new_docs)

    if docs_delete:
        await db.delete(session, list(docs_delete))

    return templates.TemplateResponse("documents.html", {"request": request, "documents": await db.get_all(session)})


@app.get("/contact.html", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})





@app.post("/send_email/")
async def create_upload_file(user_name: str = Form(), user_email: str = Form(),user_phone: str = Form(), MESSAGE: str = Form(), file: UploadFile = Form(...)):
    form = ContactForm(
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        message=MESSAGE,
        file=await MyUploadFile.from_uploadfile(file)
    )

    msg = MIMEMultipart('mixed')
    # Добавление текстовой части сообщения
    text_part = MIMEText(f"Name: {form.user_name} \nemail: {form.user_email} \ntel_number: {form.user_phone} \nmessage: {form.message}", 'plain')
    msg.attach(text_part)
    if form.file.filename:
        # Добавление вложения
        attachment_part = MIMEApplication(form.file.filetext, Name=form.file.filename)
        attachment_part['Content-Disposition'] = f'attachment; filename="{form.file.filename}"'
        msg.attach(attachment_part)

    # Заголовки сообщения
    msg['From'] = 'sharapov.kirill.site@ya.ru'
    msg['To'] = 'sharapov.kirill.site@ya.ru'
    msg['Subject'] = 'Письмо с сайта'

    # Подключение к серверу SMTP и отправка сообщения
    async with aiosmtplib.SMTP('smtp.yandex.com', 587) as smtp:
        await smtp.login('sharapov.kirill.site@ya.ru', os.getenv('PASSWORD'))
        await smtp.send_message(msg)

    return JSONResponse(status_code=200, content={"message": "Форма успешно отправлена"})

