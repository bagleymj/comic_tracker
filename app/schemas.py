from pydantic import BaseModel
from typing import List

class SeriesCreate(BaseModel):
    title: str

class IssueCreate(BaseModel):
    title: str
    issue_number: int
    series_id: int

class IssueInput(BaseModel):
    series: int
    issues: List[int]

class BookInput(BaseModel):
    title: str
    isbn: str
    issues: List[IssueInput]