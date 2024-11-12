import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["archival_object_uri", "position", "title","dates"])

    #Open CSV reader and ignore header row
    with open(archival_object_csv,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            # Isolate the resource to be worked on using find_by_id
            resource = client.get(f'/{row[0]}').json()
            position = resource.get("position")
            title = resource.get("title")
            expression = ""

            if resource.get("dates"):
                date = resource.get("dates")

                for item in date:
                    expression = item.get("expression")

            row = [row[0], position, title, expression]
            writer.writerow(row)