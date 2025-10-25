from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class JournalEntryDB(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)