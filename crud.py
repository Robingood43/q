from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from models import Document


class Crud:
    async def get_all(self, async_session:async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            docs = select(Document).order_by(Document.id)
            result = await session.execute(docs)
            return result.scalars()

    async def add(self, async_session:async_sessionmaker[AsyncSession], docs:Document):
        async with async_session() as session:
            session.add(docs)
            await session.commit()

    async def delete(self, async_session:async_sessionmaker[AsyncSession], docs:Document):
        async with async_session() as session:
            await session.delete(docs)
            await session.commit()