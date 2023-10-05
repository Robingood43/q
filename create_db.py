from db import engine, Base
import asyncio


async def create_db():
    async with engine.begin() as conn:
        from models import Document
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_db())

# from main import get_password_hash
#
# print(get_password_hash('admin'))
