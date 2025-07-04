FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y ffmpeg git curl

# Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
