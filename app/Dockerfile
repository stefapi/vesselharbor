# app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers de configuration Poetry
COPY poetry.lock pyproject.toml /app/

# Installer Poetry et les dépendances (sans créer d'environnement virtuel)
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# Copier le code de l'application
COPY . /app

EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]

