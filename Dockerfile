FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# main.py contains: app = Flask(__name__)
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]

# Cloud Run expects PORT (default 8080)
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} main:app"]