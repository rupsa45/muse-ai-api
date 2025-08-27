from services.llm import llm , story_prompt
from db import db
from fastapi import  HTTPException



# Generate story from user prompt
async def generate_story_service(prompt: str, user_id: str | None = None):
    """Handles story generation using LLM and saves to DB"""

    # Format messages with user prompt
    messages = story_prompt.format_messages(user_prompt=prompt)

    # Call the LLM
    response = await llm.ainvoke(messages)
    generated_content = response.content

    # Save draft in DB
    draft = await db.draft.create(
        data={
            "title": "Untitled Story",   # Later we can improve to auto-extract from AI
            "content": generated_content,
            "userId": user_id
        }
    )

    return draft
    

async def analyze_story(draftId: str):
    try:
        draft = await db.draft.find_unique(where={"id": draftId})
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")

        # Ask AI for tone/emotion
        response = await llm.ainvoke([
            ("system", "You are an expert literary analyst. "
             "Analyze the dominant emotion or tone of the following story in ONE LINE."),
            ("user", draft.content)
        ])

        return {"emotion": response.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))