from pydantic import BaseModel
class DraftRequest(BaseModel):
    title:str
    content:str
    mode:str
    style:str
    userId: str | None = None