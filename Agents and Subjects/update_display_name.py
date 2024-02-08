import csv
import glob
import json
import os
import pathlib
from pprint import pprint

import requests
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set input file
merge_input = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\bad_display.csv")

merge_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\bad_display.csv")

with (open(merge_input,'r') as csvfile):
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:

        aspace_name = client.get(row[1]).json()

        display = aspace_name.get("display_name")
        display["sort_name_auto_generate"] = False
        display["sort_name"] = row[0]

        # Post updates
        updated = client.post(row[1], json=aspace_name)

        if updated.status_code == 200:
            print("Archival object {} updated".format(row[1]))
        else:
            print(updated.json())
