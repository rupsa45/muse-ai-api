
from pydantic import BaseModel

# Request schema for story generation
class StoryRequest(BaseModel):
    title: str
    mode: str
    style: str
    userId: str | None = None
