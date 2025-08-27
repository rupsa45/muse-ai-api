python -m venv venv


## - To generate a requirements.txt from your current environment:
pip freeze > requirements.txt

## pip install -qU "langchain[openai]"

- -qU means:
- -q: quiet mode (less output)
- -U: upgrade to the latest version if already installed

## Install Packages from requirements.txt
pip install -r requirements.txt

uvicorn api:app --reload

pip install passlib[bcrypt]

pip install pydantic[email]

✅ Why this is good:

StoryRequest → keeps story generation API super simple (just prompt + optional userId).

DraftRequest → covers cases where you might want to save a draft manually (instead of AI).

AnalyzeRequest → keeps analysis logic isolated to an existing draft.

Generate → User gives a prompt → AI creates a draft (saved in DB).

Analyze → AI gives tone/emotion.

Revise / Continue → User says things like:

“Make the ending more dramatic.”

“Add more dialogue between characters.”

“Rewrite this part in a happy tone.”

👉 Under the hood, you’d just:

Fetch the saved draft content from DB.

Pass it along with the user’s new instruction into the LLM.

Replace or save the new version as an updated draft.

Example flow in code (pseudo):

async def revise_draft(draftId: str, user_instruction: str):
    draft = await db.draft.find_unique(where={"id": draftId})
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    response = await llm.ainvoke([
        ("system", "You are editing a story based on user feedback. Keep original content but apply requested changes."),
        ("user", f"Original story:\n{draft.content}\n\nUser request: {user_instruction}")
    ])

    updated_content = response.content

    updated_draft = await db.draft.update(
        where={"id": draftId},
        data={"content": updated_content}
    )

    return updated_draft


So yes ✅ the user can keep the conversation alive with the draft (generate → analyze → revise → repeat).

A user can generate a draft (via your existing story route).

Read or analyze it.

Then send a POST request to /draft/revise with { "draftId": "...", "instruction": "Make the ending happier" }.

The draft gets updated in DB with AI’s revised version.