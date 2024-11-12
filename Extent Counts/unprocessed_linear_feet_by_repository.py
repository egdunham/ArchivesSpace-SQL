import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
#csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

lf_total = 0

tempExtent = 0

resourceSet = client.get(f'/repositories/5/accessions?all_ids=true').json()

for id in resourceSet:
    collection = client.get(f'/repositories/5/accessions/{id}').json()
    extents = collection.get("extents")

    for extent in extents:
        if extent["extent_type"] == "linear_feet":
            tempExtent = extent["number"]

    if "collection_management" in collection:
        collMgt = collection["collection_management"]

        if "processing_status" in collMgt and collMgt["processing_status"] != "completed" and collMgt["processing_status"] != "Inventory on AAO":
            lf_total = lf_total + float(tempExtent)
            print("No processed!", collMgt["processing_status"])
            break

        if "processing_status" not in collMgt:
            lf_total = lf_total + float(tempExtent)
            print("no processing note", collMgt)

    else:

        if "user_defined" in collection:
            notes = collection.get("user_defined")

            if "text_2" in notes and notes["text_2"] != "INV_AAO":
                print("no note at all-2", collection)


            elif "text_4" in notes and notes["text_4"] != "INV_AAO":
                print("no note at all-4", collection)

            else:
            # PULL OUT ALL THE 2 and 4s that have INV_AAO
                lf_total = lf_total + float(tempExtent)

print(lf_total)