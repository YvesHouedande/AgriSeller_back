# Utilisez une version LTS de Python (3.11 recommandé)
FROM python:3.11-slim-bullseye

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créez et activez le répertoire de travail
WORKDIR /app

# Installez les dépendances système pour Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiez les fichiers de dépendances
COPY requirements.txt .

# Installez les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copiez le projet
COPY . .

EXPOSE 8000 8001

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & daphne -b 0.0.0.0 -p 8001 AgriSeller_back.asgi:application"]