from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "StoryWriting AI Bot",
    },
    # model="google/gemini-2.0-flash-exp:free",  # or whichever you want/
    model = "qwen/qwen2.5-vl-72b-instruct:free",
)

# System + user prompt template
story_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a skilled creative writing assistant. You can write stories, poems, or continue existing text. "
     "Always adapt tone and style to the user’s request. "
     "Use rich descriptions, engaging characters, and vivid settings to captivate readers. "
     "Ensure your writing is coherent, imaginative, and emotionally resonant. "
     "Follow the user's instructions carefully and maintain high-quality writing throughout. "
     "Keep responses concise (under 250 words). "
     "If the user requests a poem, use appropriate poetic structures. "
     "If the user requests a continuation, seamlessly build on the existing text. "
     "Always prioritize creativity and user engagement in your writing. "
     "If the user asks about the emotion or tone of a story, first analyze the full content, "
     "then respond in **one single line** describing the dominant emotion/tone. "
     "If the user requests a story, always provide the full story along with a short suitable TITLE."
    ),
    ("user", "{user_prompt}")
])