# Étape 1 : Construction de l'application
FROM python:3.11-alpine3.17 AS build

WORKDIR /usr/local/vote

# Copier le fichier des dépendances et installer les paquets sans cache
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt 

FROM python:3.11-alpine3.17
RUN addgroup -S appgroup && adduser --disabled-password -S appuser -G appgroup
USER appuser

# Définir l'environnement Flask en production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/local/vote
COPY --chown=appuser . /usr/local/vote
COPY --from=build --chown=appuser /root/.local /home/appuser/.local

EXPOSE 8080

CMD ["python", "app.py"]
