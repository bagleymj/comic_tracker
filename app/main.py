from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import series, issues, books

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        #WIPE TABLES
        await conn.run_sync(Base.metadata.drop_all)
        #CREATE TABLES
        await conn.run_sync(Base.metadata.create_all)

app.include_router(series.router)
app.include_router(issues.router)
app.include_router(books.router)