from pydantic import BaseModel


# Request schema for saving a draft manually (if needed)
class DraftRequest(BaseModel):
    title: str
    content: str
    userId: str | None = None

# Request schema for analyzing a Draft
class AnalyzeRequest(BaseModel):
    draftId: str