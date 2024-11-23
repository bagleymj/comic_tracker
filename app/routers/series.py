from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models import Issue, Series
from app.schemas import SeriesCreate

router = APIRouter()
@router.post("/series")
async def create_series(series: SeriesCreate, session: AsyncSession = Depends(get_session)):
    new_series = Series(title=series.title)
    session.add(new_series)
    await session.commit()
    await session.refresh(new_series)
    return new_series
