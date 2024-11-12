import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        resource = client.get(f'/{row[0]}').json()
        resource["position"] = int(row[1])

        # Post updates
        updated = client.post(resource["uri"], json=resource)

        if updated.status_code == 200:
            print("Archival object {} updated".format(resource["uri"]))
        else:
            print(updated.json())

    csvfile.close()