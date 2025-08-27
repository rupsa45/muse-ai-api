
from pydantic import BaseModel

# Request schema for story generation (user gives only a prompt)
class StoryRequest(BaseModel):
    prompt: str
    userId: str | None = None
