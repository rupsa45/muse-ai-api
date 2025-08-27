
from pydantic import BaseModel

# Request schema for revision
class ReviseRequest(BaseModel):
    draftId: str
    instruction: str