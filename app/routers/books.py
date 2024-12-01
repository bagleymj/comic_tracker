from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app.database import get_session
from app.models import Book, Issue, book_issue_association
from app.schemas import BookInput

router = APIRouter()

@router.get("/books")
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    return result.scalars().all()

@router.post("/books")
async def create_book(book_input: BookInput, session: AsyncSession = Depends(get_session)):
    new_book = Book(title=book_input.title, isbn=book_input.isbn)
    session.add(new_book)
    
    for issue_input in book_input.issues:
        series_id = issue_input.series
        for issue_number in issue_input.issues:
            result = await session.execute (
                select(Issue).where(
                    Issue.series_id == series_id,
                    Issue.issue_number == issue_number
                )
            )
            issue = result.scalars().first()

            if not issue:
                raise HTTPException(
                    status_code=404,
                    detail=f"Issue with series_id={series_id} and issue_number={issue_number} not found"
                )
            #Issue occurring here
            await session.refresh(new_book, ["issues"])
            new_book.issues.append(issue)
            #await session.execute(
            #    insert(book_issue_association).values(book_id=new_book.id, issue_id=issue.id)
            #)
            #await session.refesh(new_book, ["issues"])
    await session.commit()

    

    return {"message": "Book created successfully", "book_id": new_book.id}
    #return {"message" "Book created."}