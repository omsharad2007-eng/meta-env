FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY models.py .
COPY server/ ./server/

RUN pip install --no-cache-dir fastapi uvicorn pydantic requests openai

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
