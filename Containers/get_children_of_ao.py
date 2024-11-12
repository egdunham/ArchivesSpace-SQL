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
    writer.writerow(["archival_object_uri", "title", "date", "subseries"])

    #Open CSV reader and ignore header row
    with open(archival_object_csv,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            # Isolate the resource to be worked on using find_by_id
            resource = client.get(f'/{row[0]}/children').json()
            subseries = row[1]
            for item in resource:
                #record = client.get(f'/repositories/2/archival_objects/{item}').json()
                # URI and title

                uri = item["uri"]
                title = item["title"]
                itemDate = ""

                if item["dates"]:
                    for date in item.get("dates"):
                        itemDate = date.get("expression")

                #note = record.get("notes")

                #if note:
                    #for id in note:
                        #content = id.get("content")

                row = [uri, title, itemDate, subseries]
                writer.writerow(row)
                #print(uri,"|",title,"|",itemDate)
