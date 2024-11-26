from pydantic import BaseModel

class SeriesCreate(BaseModel):
    title: str

class IssueCreate(BaseModel):
    title: str
    issue_number: int
    series_id: int