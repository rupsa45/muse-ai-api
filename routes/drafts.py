from fastapi import APIRouter, HTTPException
from services.llm import llm 
from models.revise import ReviseRequest

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


## Revise a draft (creates a new draft instead of overwriting)
@router.post("/revise")
async def revise_draft(request: ReviseRequest):
    draft = await db.draft.find_unique(where={"id": request.draftId})
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    # Send original + instruction to LLM
    response = await llm.ainvoke([
        ("system", "You are editing a story based on user feedback. Keep original content but apply requested changes."),
        ("user", f"Original story:\n{draft.content}\n\nUser request: {request.instruction}")
    ])

    updated_content = response.content

    # Create a NEW draft (instead of updating old one)
    new_draft = await db.draft.create(
        data={
            "title": f"{draft.title} (Revised)",
            "content": updated_content,
            "userId": draft.userId
        }
    )

    return {
        "message": "Draft revised and saved as a new version",
        "draft": new_draft
    }