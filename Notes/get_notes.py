import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


# Input is [uri]
input = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["persistent_id", "PID", "content"])

    with open(input,'r', encoding='utf-8-sig') as csvin:
        reader = csv.reader(csvin)
        next(reader, None)

        # Establish search terms
        for row in reader:
            id = row[0]

            ao = client.get(f"{id}").json()
            note = ao.get("notes")

            # Single part note
            for item in note:
                PID = item.get("persistent_id")
                content = item.get("content")
                #pprint(item)

                # Multi part notes
                if item.get("subnotes"):
                    subnote = item.get("subnotes")

                    #pprint(subnote)
                    for note in subnote:
                        content = note.get("content")

                row = [row[0], PID, content]
                writer.writerow(row)

