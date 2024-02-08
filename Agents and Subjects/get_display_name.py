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
merge_input = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\merge_output.csv")


merge_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\bad_display.csv")

with (open(merge_input,'r') as csvfile):
    reader = csv.reader(csvfile)
    next(reader, None)

    with open(merge_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        headerRow = {"LOC Display", "LOC URI", "ASpace Display", "ASpace URI"}
        writer.writerow(headerRow)

        for row in reader:

            # Get MARC display name
            record = requests.get(row[0] + ".skos.json").json()

            for id in record:
                source = id.get("@type")

                for record in source:
                    if record == "http://www.w3.org/2004/02/skos/core#Concept":
                        label = id.get("http://www.w3.org/2004/02/skos/core#prefLabel")

                        for item in label:
                            pref = item.get("@value")

                            #Get ASpace display name
                            aspace_name = client.get(row[1]).json()
                            display = aspace_name.get("display_name").get("sort_name")

                            #Check to see if display names match
                            match = display == pref

                            if not match:

                                row = [pref, row[0], display, row[1]]

                                writer.writerow(row)

                                #print("LOC: " + pref + " ASpace: " + display + "  Match: " + str(match))
