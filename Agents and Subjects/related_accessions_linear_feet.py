import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

lf = 0
boxes = 0

resource = client.get(f'/repositories/4/resources/{932}').json()
accession = resource.get("related_accessions")

for item in accession:
    ref = item.get("ref")

    accession_json = client.get(ref).json()

    extents = accession_json.get("extents")

    for extent in extents:
        if extent.get("extent_type") == "linear_feet":
            lf = lf + float(extent.get("number"))

        if extent.get("extent_type") == "Box(es)":
            boxes = boxes + float(extent.get("number"))

print("Boxes: ")
print(boxes)
print("\nLinear Feet: ")
print(lf)
