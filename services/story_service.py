from services.llm import llm , prompt
from db import db
from fastapi import  HTTPException



# Generate story from user prompt
async def generate_story(prompt_text: str, userId: str | None = None):
    try:
        chain = prompt | llm
        response = await chain.ainvoke({
            "input": prompt_text
        })

        # Extract text (AI will return full story + title suggestion inside response.content)
        ai_output = response.content

        # For simplicity: split title and content if AI includes "Title:"
        title = "Untitled Story"
        content = ai_output

        if "Title:" in ai_output:
            parts = ai_output.split("Title:", 1)
            if len(parts) > 1:
                # Extract title and story separately
                maybe_title = parts[1].split("\n", 1)[0].strip()
                if maybe_title:
                    title = maybe_title
                content = ai_output

        # Save draft to DB
        draft = await db.draft.create(
            data={
                "title": title,
                "content": content,
                "userId": userId,
            }
        )
        return draft

    except Exception as e:
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