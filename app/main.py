from fastapi import FastAPI, Depends
from app.models import Base, Issue, Series
from app.database import engine, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.routers import series, issues

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(series.router)
app.include_router(issues.router)