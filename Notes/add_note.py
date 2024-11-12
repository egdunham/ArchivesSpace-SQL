import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

with open(archival_object_csv,'r', encoding='utf-8-sig') as csvin:
    reader = csv.reader(csvin)
    next(reader, None)

    # Establish search terms
    for row in reader:
        id = row[0]
        ao = client.get(f"{id}").json()
        note = ao.get("notes")
        #subnote = note.get("subnotes")
        physdesc = {'content': [row[1]], 'jsonmodel_type': 'note_singlepart', 'publish': False, 'type': 'physdesc'}
        note.append(physdesc)

        # Post updates
        updated = client.post(ao["uri"], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao["uri"]))
        else:
            print(updated.json())

    csvin.close()
