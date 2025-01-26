FROM python:3.11-alpine@sha256:9af3561825050da182afc74b106388af570b99c500a69c8216263aa245a2001b
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]