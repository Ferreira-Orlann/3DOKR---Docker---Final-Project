# Étape 1 : Construction de l'application
FROM python:3.11-alpine3.17 AS build

WORKDIR /vote

# Copier le fichier des dépendances et installer les paquets sans cache
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt 

# Copier le reste de l'application
COPY . .

RUN adduser --disabled-password appuser

USER appuser

# Définir l'environnement Flask en production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

WORKDIR /vote

COPY --chown=appuser . /code

COPY --from=build --chown=appuser /root/.local /home/appuser/.local

EXPOSE 8080

# Lancer l'application en production avec waitress (meilleur que `python app.py`)
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8080", "app:app"]
