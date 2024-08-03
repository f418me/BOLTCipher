#!/bin/bash

# Pfad zur CSV-Datei
csv_file="bolt11.csv"

# Schleife, um das Kommando 5 Mal auszuführen
for i in {1..5}; do
    # Generiere einen zufälligen 32-Byte-Wert und konvertiere ihn in Hexadezimal
    preimage=$(openssl rand -hex 32)

    # Führe das lncli-Kommando mit dem generierten Preimage aus
    response=$(lncli --macaroonpath=/Users/fre/voltage/admin.macaroon --tlscertpath="" --rpcserver=tschinoko.m.voltageapp.io addinvoice --amt 18 --memo "Test Invoice" --preimage $preimage)

    # Extrahiere den payment_request Wert aus der Antwort
    payment_request=$(echo $response | jq -r '.payment_request')

    # Füge Preimage und Payment Request zur CSV-Datei hinzu
    echo "$preimage,$payment_request" >> $csv_file
done
