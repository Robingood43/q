from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, delete, func
from models import Document, User, News


class Crud:
    async def get_all_docs(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            news = select(
                Document.id,
                Document.size,
                Document.filename,
                func.to_char(Document.date_add, 'DD.MM.YYYY').label('date_add')
            ).order_by(Document.date_add)
            result = await session.execute(news)
            result = result.fetchall()
            return result

    async def get_all_news(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            news = select(
                News.id,
                News.size,
                News.filename,
                func.to_char(News.date_add, 'DD.MM.YYYY').label('date_add')
            ).order_by(News.date_add)
            result = await session.execute(news)
            result = result.fetchall()
            print(result)
            return result


    async def add_docs(self, async_session: async_sessionmaker[AsyncSession], docs: [Document]):
        async with async_session() as session:
            session.add_all(docs)
            await session.commit()

    async def add_news(self, async_session: async_sessionmaker[AsyncSession], news: [News]):
        async with async_session() as session:
            session.add_all(news)
            await session.commit()

    async def delete_docs(self, async_session: async_sessionmaker[AsyncSession], filename: list):
        async with async_session() as session:
            await session.execute(delete(Document).where(Document.filename.in_(filename)))
            await session.commit()

    async def delete_news(self, async_session: async_sessionmaker[AsyncSession], filename: list):
        async with async_session() as session:
            await session.execute(delete(News).where(News.filename.in_(filename)))
            await session.commit()

    async def user_check(self, async_session: async_sessionmaker[AsyncSession], user: User):
        async with async_session() as session:
            res = await session.execute(select(User).where(User.username == user))
            await session.commit()
            result = res.scalars().first()  # достаем первого пользователя из результатов
            print(result)
            return result

    # async def user_add(self, async_session: async_sessionmaker[AsyncSession], user: User):
    #     db.query(User).filter(User.username == form_data.username).first()
    #     async with async_session() as session:
    #         session.add(user)
    #         await session.commit()