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

resourceSet = client.get(f'/repositories/5/resources?all_ids=true').json()

for id in resourceSet:
    collection = client.get(f'/repositories/5/resources/{id}').json()

    # Remove duplicative Spanish Guides
    if ("id_1" in collection and "SPA" not in collection["id_1"] and "#" not in collection["id_1"]) or "id_1" not in collection:

        if ("id_2" in collection and "SPA" not in collection["id_2"] and "#" not in collection["id_2"]) or "id_2" not in collection:
            extents = collection.get("extents")

            for extent in extents:
                if extent["extent_type"] == "linear_feet":
                    lf_total = lf_total + float(extent["number"])
print("Total linear feet: ", lf_total)