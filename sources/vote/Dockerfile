# Étape 1 : Construction de l'application
FROM python:3.11-alpine3.17 AS build

WORKDIR /vote

# Copier le fichier des dépendances et installer les paquets sans cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Étape 2 : Production
FROM python:3.11-alpine@sha256:9af3561825050da182afc74b106388af570b99c500a69c8216263aa245a2001b AS prod

# Ajouter un utilisateur non-root sécurisé
RUN adduser --disabled-password --no-create-home appuser

# Définir l'environnement Flask en production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

WORKDIR /vote

# Copier l'application et les dépendances depuis l'étape build
COPY --from=build /vote /vote

# Changer les permissions pour éviter les problèmes de droits
RUN chown -R appuser:appuser /vote

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port utilisé par Flask
EXPOSE 8080

# Lancer l'application en production avec waitress (meilleur que `python app.py`)
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8080", "app:app"]
