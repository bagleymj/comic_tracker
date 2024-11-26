from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    issues = relationship("Issue", back_populates="series")

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    issue_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    series = relationship("Series",back_populates="issues")