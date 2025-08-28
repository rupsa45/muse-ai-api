from db import db

# Define this at the top level
def extract_title(content: str) -> str:
    # Take first line as title, max 50 chars
    first_line = content.split("\n")[0]
    title = first_line[:50].rstrip(".,! ")  # remove trailing punctuation
    return title or "Untitled Story"

# Helper function to save draft
async def save_draft(db, user_id: str, prompt: str, generated_content: str):
    draft_title = extract_title(generated_content)
    draft = await db.draft.create(
        data={
            "title": draft_title,
            "prompt": prompt,
            "content": generated_content,
            "userId": user_id
        }
    )
    return draft

# Route to create a draft
async def create_draft_route(request):
    data = await request.json()
    generated_content = data.get("content", "")
    prompt = data.get("prompt", "")
    user_id = data.get("userId", "")

    draft = await save_draft(db, user_id, prompt, generated_content)
    return {"draft": draft}
