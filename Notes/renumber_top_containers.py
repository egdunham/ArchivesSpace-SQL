from pprint import pprint

import asnake.utils
import os
import csv
import json

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Format CSV as [id][old number][new number]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\renumber.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:

        # Isolate the resource to be worked on using find_by_id
        ao = client.get(f"/repositories/2/top_containers/{row[0]}").json()

        new_short = ao.get("display_string").replace(row[1], row[2])
        new_long = ao.get("long_display_string").replace(row[1], row[2])

        ao["indicator"] = row[2]
        ao["display_string"] = new_short
        ao["long_display_string"] = new_long

        # Post updates
        updated = client.post(ao["uri"], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(row[1]))
        else:
            print(updated.json())
