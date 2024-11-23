from pydantic import BaseModel

class SeriesCreate(BaseModel):
    title: str

class IssueCreate(BaseModel):
    title: str
    issue_number: int
    owned: bool = False
    read: bool = False
    series_id: int