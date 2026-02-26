FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libcairo2-dev

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Si usas una imagen basada en Debian/Ubuntu (ej. python:3.11)
# Si usas una imagen basada en Python (Debian/Ubuntu)
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    gzip \
    openssl \
    && rm -rf /var/lib/apt/lists/*