from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models import Issue, Series
from app.schemas import IssueCreate

router = APIRouter()

@router.get("/issues")
async def get_issues(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Issue))
    return result.scalars().all()

@router.post("/issues")
async def create_issue(issue: IssueCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Series).where(Series.id == issue.series_id))
    series = result.scalars().first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    new_issue = Issue(
        title=issue.title,
        issue_number=issue.issue_number,
        series_id=issue.series_id
    )
    session.add(new_issue)
    await session.commit()
    await session.refresh(new_issue)
    return new_issue