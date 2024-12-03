from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
import httpx
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
            await session.refresh(new_book, ["issues"])
    await session.commit()
    return {"message": "Book created successfully", "book_id": new_book.id}

@router.post("/books_by_isbn")
async def add_book_by_isbn(isbn: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.isbn == isbn))
    existing_book = result.scalars().first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists in the database.")
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(f"https://openlibrary.org/isbn/{isbn}.json")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch book data from OpenLibrary")
        
    data = response.json()
    title = data.get("title")
    if not title:
        raise HTTPException(status_code=422, detail="Book title not found in OpenLibrary.")
    
    new_book = Book(title=title, isbn=isbn)
    session.add(new_book)
    await session.commit()

    return {"message": "Book added successfully", "book_id": new_book.id, "title": title}

@router.get("/book")
async def get_book(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Book).where(Book.id == id)
    )
    return result.scalars().first()
