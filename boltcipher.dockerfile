# Verwende das offizielle Python 10 Base-Image
FROM python:3.10.14-alpine3.20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere Git und lade das Projekt herunter
RUN apk update \
    && apk add --no-cache git \
    && apk add --no-cache bash \
    && apk add --no-cache vim \
    && git clone https://github.com/f418me/BOLTCipher.git \
    && cd BOLTCipher \
    && pip install --no-cache-dir -r requirements.txt

# Exponiere Port 8000 für den Zugang zum Service
EXPOSE 8000

# Setze das Arbeitsverzeichnis auf das geklonte Repo
WORKDIR /app/BOLTCipher

# Starte das Hauptscript (ersetze `main.py` mit dem tatsächlichen Scriptnamen)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
