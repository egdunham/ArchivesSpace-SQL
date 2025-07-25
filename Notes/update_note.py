import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


# Set file of names to search
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Desktop\input.csv")


with open(archival_object_csv,'r', encoding='utf-8-sig') as csvin:
    reader = csv.reader(csvin)
    next(reader, None)

    # Establish search terms
    for row in reader:
        id = row[0]

        ao = client.get(f"/repositories/2/archival_objects/{id}").json()
        note = ao.get("notes")

        for item in note:
            if item["type"] == "separatedmaterial":
                subnote = item.get("subnotes")
                for item in subnote:
                    item["content"] = row[1]

        # Post updates
        updated = client.post(ao["uri"], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao["uri"]))
        else:
            print(updated.json())

    csvin.close()
