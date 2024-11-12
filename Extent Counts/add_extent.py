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
        extent = ao.get("extents")

        newExtent = {'extent_type': 'Videotape(s): VHS', 'jsonmodel_type': 'extent', 'number': '1', 'portion': 'whole'}
        extent.append(newExtent)

        # Post updates
        updated = client.post(ao["uri"], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao["uri"]))
        else:
            print(updated.json())

    csvin.close()