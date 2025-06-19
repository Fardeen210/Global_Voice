FROM python:3.11-slim

WORKDIR /app

# 🛠️ Install ffmpeg and system deps
RUN apt-get update && apt-get install -y ffmpeg git curl

# ⚡ Install uv and deps
COPY requirements.txt ./
RUN pip install -r requirements.txt


# 📦 Copy app code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
