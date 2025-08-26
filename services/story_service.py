from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from db import db
from fastapi import  HTTPException
import os

from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "StoryWriting AI Bot",
    },
    model="google/gemini-2.0-flash-exp:free",  # or whichever you want
)


prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a skilled creative writing assistant. You can write stories, poems,literary editor or continue existing text. "
     "Always adapt tone and style to the user’s request."
     " Use rich descriptions, engaging characters, and vivid settings to captivate readers."
     " Ensure your writing is coherent, imaginative, and emotionally resonant."
     " Follow the user's instructions carefully and maintain high-quality writing throughout."
     " Keep responses concise (under 550 words)."
     " If the user requests a poem, use appropriate poetic structures."
     " If the user requests a continuation, seamlessly build on the existing text."
     " Always prioritize creativity and user engagement in your writing."
     ),
    ("user", 
     "Title: {title}\n"
     "Mode: {mode}\n"
     "Style: {style}\n"
     "Please generate content according to the mode (Story, Poem, or Continuation).")
])


async def generate_story(title: str, mode: str, style: str, userId: int):
    try:
        # Build the prompt
        chain = prompt | llm
        response = await chain.ainvoke({
            "title": title,
            "mode": mode,
            "style": style,
        })
        # Save to DB
        draft = await db.draft.create(
            data={
                "title": title,
                "content": response.content,
                "mode": mode,
                "style": style,
                "userId": userId,
            }
        )
        return draft
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
