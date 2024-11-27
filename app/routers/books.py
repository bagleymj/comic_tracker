from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models import Book

router = APIRouter()

@router.get("/books")
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    return result.scalars().all()