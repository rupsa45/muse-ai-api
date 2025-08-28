from services.llm import llm , story_prompt
from db import db
from fastapi import  HTTPException
import logging

from langchain.schema import SystemMessage, HumanMessage


# Generate story from user prompt
async def generate_story_service(prompt: str, user_id: str | None = None):
    """Handles story generation using LLM and saves to DB"""
    try:
        # Format messages with user prompt
        messages = story_prompt.format_messages(user_prompt=prompt)

        # Call the LLM
        response = await llm.ainvoke(messages)
        generated_content = response.content

         # --- Title generation (separate prompt) ---
        title_messages = [
            SystemMessage(content="You are a creative AI. Provide a short, catchy title for the following story."),
            HumanMessage(content=generated_content),
        ]
        title_response = await llm.ainvoke(title_messages)
        title = title_response.content.strip() or "Untitled Story"
        # Save draft in DB
        draft = await db.draft.create(
            data={
                "title": title,            # AI-generated title
                "prompt": prompt,              # ✅ store user input
                "content": generated_content,  # ✅ store AI output
                "userId": user_id
            }
        )
        return draft
    
    except Exception as e:
        logging.error(f"Error generating story: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

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