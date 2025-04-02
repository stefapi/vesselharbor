.PHONY: install run test lint format clean

# Installe les dépendances via Poetry
install:
	poetry install

# Lance le serveur en récupérant le port défini dans la variable d'environnement (par défaut 8000)
run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port $$(python -c "import os; print(os.getenv('PORT', '8010'))")

# Exécute les tests
test:
	poetry run pytest

# Vérifie la conformité du code avec isort et black
lint:
	poetry run isort --check-only .
	poetry run black --check .

# Formate le code avec isort et black
format:
	poetry run isort .
	poetry run black .

# Nettoie les fichiers temporaires et caches
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
