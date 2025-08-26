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