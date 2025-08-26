from fastapi import APIRouter, HTTPException
from models.story import StoryRequest

from db import db

router = APIRouter()


##Get all drafts for a user
@router.get("/{userId}")
async def get_drafts(userId: str):
    drafts = await db.draft.find_many(where={"userId": userId})
    return drafts


##Get a single draft by ID
@router.get("/{draftId}")
async def get_draft(draftId: str):
    draft = await db.draft.find_unique(where={"id": draftId})
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft

##Delete a draft
@router.delete("/draft/{draftId}")
async def delete_draft(draftId: str):
    await db.draft.delete(where={"id": draftId})
    return {"message": "Draft deleted successfully"}