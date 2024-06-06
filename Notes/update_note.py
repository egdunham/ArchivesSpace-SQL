import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


# Set file of names to search
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\archival_object_csv.csv")

with open(archival_object_csv,'r', encoding='utf-8-sig') as csvin:
    reader = csv.reader(csvin)
    next(reader, None)

    # Establish search terms
    for row in reader:
        id = row[0]

        ao = client.get(f"/repositories/4/archival_objects/{id}").json()
        note = ao.get("notes")

        for id in note:
            PID = id.get("persistent_id")
            content = id.get("content")

            if PID == row[1]:

                to_add = row[2]
                content.clear()
                content.append(to_add)

        # Post updates
        updated = client.post(ao["uri"], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao["uri"]))
        else:
            print(updated.json())

    csvin.close()
