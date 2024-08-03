import csv

def read_bolt11(file_path):
    updated_rows = []
    result_dict = None
    found_unread = False  # Zustand, um zu überprüfen, ob eine ungelesene Zeile gefunden wurde

    # CSV-Datei öffnen und Zeilen lesen
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        for row in reader:
            if not found_unread:  # Prüfen, ob bereits eine ungelesene Zeile gefunden wurde
                if len(row) == 2 and not row[0].startswith('used'):  # Überprüfen, ob die Zeile zwei Elemente hat und nicht markiert ist
                    result_dict = {'Preimage': row[0], 'bolt11': row[1]}
                    row = ['used'] + row  # Markieren der Zeile als "used" am Anfang der Zeile
                    found_unread = True  # Setzen des Flags, dass eine ungelesene Zeile gefunden wurde
            updated_rows.append(row)  # Füge die gelesenen Zeilen zur Aktualisierungsliste hinzu

    # CSV-Datei mit den aktualisierten Zeilen zurückschreiben
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    return result_dict

# Beispiel zur Verwendung der Funktion
result = read_bolt11('../bolt11.csv')
print(result)
