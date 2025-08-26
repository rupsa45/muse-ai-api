from fastapi import APIRouter, HTTPException
from models.story import StoryRequest
from services.story_service import generate_story

router = APIRouter()

@router.post("/generate")
async def generate(req: StoryRequest):
    try:
        draft = await generate_story(req.title, req.mode, req.style, req.userId)
        return {"message": "Story generated successfully", "draft": draft}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
