from fastapi import FastAPI
from app.models import Base
from app.database import engine, SessionLocal
from app.routers import series, issues
from sqlalchemy.sql import text

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # DUMP DATA
        table_data = {}
        async with SessionLocal() as session:
            for table_name, table in Base.metadata.tables.items():
                result = await session.execute(text(f"SELECT * FROM {table_name};"))
                table_data[table_name] = [dict(row) for row in result.fetchall()]
        #WIPE TABLES
        await conn.run_sync(Base.metadata.drop_all)
        #CREATE TABLES
        await conn.run_sync(Base.metadata.create_all)
        async with SessionLocal() as session:
            for table_name, rows in table_data.items():
                if rows:
                    await session.execute(
                        Base.metadata.tables[table_name].insert(),
                        rows
                    )
            await session.commit()

app.include_router(series.router)
app.include_router(issues.router)