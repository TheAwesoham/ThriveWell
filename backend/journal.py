from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend import models
from backend.database import SessionLocal

class JournalEntry(BaseModel):
    title: str
    content: str

router = APIRouter()

@router.post("/")
def create_entry(entry: JournalEntry):
    db = SessionLocal()
    try:
        db_entry = models.JournalEntryDB(title=entry.title, content=entry.content)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return {"message": "Entry created successfully", "id": db_entry.id}
    finally:
        db.close()


@router.get("/")
def get_all_entries():
    db = SessionLocal()
    try:
        entries = db.query(models.JournalEntryDB).all()
        return {entry.id: {"title": entry.title, "content": entry.content} for entry in entries}
    finally:
        db.close()


@router.get("/{entry_id}")
def get_entry(entry_id: int):
    db = SessionLocal()
    try:
        entry = db.query(models.JournalEntryDB).filter(models.JournalEntryDB.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"title": entry.title, "content": entry.content}
    finally:
        db.close()


@router.put("/{entry_id}")
def update_entry(entry_id: int, entry: JournalEntry):
    db = SessionLocal()
    try:
        db_entry = db.query(models.JournalEntryDB).filter(models.JournalEntryDB.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        db_entry.title = entry.title
        db_entry.content = entry.content
        db.commit()
        return {"message": "Entry updated successfully"}
    finally:
        db.close()


@router.delete("/{entry_id}")
def delete_entry(entry_id: int):
    db = SessionLocal()
    try:
        db_entry = db.query(models.JournalEntryDB).filter(models.JournalEntryDB.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        db.delete(db_entry)
        db.commit()
        return {"message": "Entry deleted successfully"}
    finally:
        db.close()