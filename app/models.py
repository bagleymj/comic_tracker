from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

book_issue_association = Table(
    "book_issue",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("issue_id", Integer, ForeignKey("issues.id"), primary_key=True) 
)
class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    issues = relationship("Issue", back_populates="series")

class Issue(Base):
    __tablename__ = "issues"
    __tableargs__ = (
        UniqueConstraint('series_id', 'issue_number', name='unique_series_issue'),
        Index('idx_series_issue', 'series_id', 'issue_number')
    )
    id = Column(Integer, primary_key=True, index=True)
    issue_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    series = relationship("Series",back_populates="issues")
    books = relationship("Book", secondary=book_issue_association, back_populates="issues", lazy="selectin")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    issues = relationship("Issue", secondary=book_issue_association, back_populates="books", lazy="selectin")
