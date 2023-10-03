import os
import glob
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates
import datetime
from db import engine
from crud import Crud
from models import Ad, Document
from sqlalchemy.ext.asyncio import async_sessionmaker


app = FastAPI(docs_url=None, redoc_url=None)
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
    all_docs_db = {i.filename for i in await db.get_all(session)}
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
