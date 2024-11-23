from fastapi import FastAPI, Depends
from app.models import Base, Issue, Series
from app.database import engine, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.routers import series

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/issues")
async def get_issues(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Issue))
    return result.scalars().all()

@app.get("/series")
async def get_series(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Series))
    return result.scalars().all()

app.include_router(series.router)