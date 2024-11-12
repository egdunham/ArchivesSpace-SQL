import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

resource = client.get(f'/repositories/4/archival_objects/{457724}/children').json()

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["archival_object_uri", "date"])

    for item in resource:
        instance = item.get("instances")

        for subcontainer in instance:
            sub = subcontainer.get("sub_container")
            topcontainer = sub.get("top_container")
            #pprint(topcontainer.get("ref"))

            row = [item.get("uri"), topcontainer.get("ref")]
            writer.writerow(row)


