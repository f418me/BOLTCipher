# Verwende das offizielle Python 10 Base-Image
FROM python:10

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere Git und lade das Projekt herunter
RUN apt-get update \
    && apt-get install -y git \
    && git clone https://github.com/f418me/BOLTChipher.git \
    && cd BOLTChipher \
    && pip install -r requirements.txt

# Exponiere Port 8000 für den Zugang zum Service
EXPOSE 8000

# Setze das Arbeitsverzeichnis auf das geklonte Repo
WORKDIR /app/BOLTChipher

# Starte das Hauptscript (ersetze `main.py` mit dem tatsächlichen Scriptnamen)
CMD ["uvicorn paydec:app --reload"]
