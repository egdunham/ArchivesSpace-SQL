import csv

import asnake.utils
import os

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#Set destination
csv_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\csv_output.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    #write CSV header row
    writer.writerow(["archival_object_uri", "title"])

    # Isolate the resource to be worked on
    resource = client.get(f'/repositories/2/resources/{1248}').json()

    # Walk tree and compose row to be exported
    for obj in asnake.utils.walk_tree(resource, client):
        uri = obj["uri"]
        title = obj["title"]
        row = [uri, title]

        # Write row to file
        writer.writerow(row)
