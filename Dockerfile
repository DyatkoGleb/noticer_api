
FROM python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install python-dotenv

CMD ["watchmedo", "auto-restart", "--recursive", "--directory", ".", "--pattern", "*.py", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]