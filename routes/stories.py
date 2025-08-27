from fastapi import APIRouter, HTTPException
from models.story import StoryRequest
from services.story_service import generate_story, analyze_story

from models.draft import AnalyzeRequest

router = APIRouter()

# Generate a story
@router.post("/generate")
async def generate(req: StoryRequest):
    try:
        draft = await generate_story(req.prompt, req.userId)
        return {"message": "Story generated successfully", "draft": draft}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analyze the tone/emotion of a story draft
@router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        result = await analyze_story(req.draftId)
        return {"message": "Analysis complete", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))