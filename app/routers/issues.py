from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models import Issue, Series
from app.schemas import SeriesCreate

router = APIRouter()

@router.get("/issues")
async def get_issues(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Issue))
    return result.scalars().all()