FROM python:3.11-slim

WORKDIR /app

# Install system deps (needed for prisma engine fetch)
RUN apt-get update && apt-get install -y \
    nodejs npm build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate Prisma client & fetch query engine
RUN prisma generate && prisma py fetch

EXPOSE 10000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
