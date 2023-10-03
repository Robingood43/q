from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, delete
from models import Document


class Crud:
    async def get_all(self, async_session:  async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            docs = select(Document).order_by(Document.date)
            result = await session.execute(docs)
            return result.scalars()

    async def add(self, async_session: async_sessionmaker[AsyncSession], docs: [Document]):
        async with async_session() as session:
            session.add_all(docs)
            await session.commit()

    async def delete(self, async_session: async_sessionmaker[AsyncSession], filename: list):
        async with async_session() as session:
            await session.execute(delete(Document).where(Document.filename.in_(filename)))
            await session.commit()
