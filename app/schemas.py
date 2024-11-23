from pydantic import BaseModel

class SeriesCreate(BaseModel):
    title: str