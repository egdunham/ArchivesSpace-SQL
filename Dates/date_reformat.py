import csv
from pprint import pprint

import asnake.utils
import os

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Read in CSV - format as [refid][start][end][certainty][type]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        # Isolate the resource to be worked on using find_by_id
        ao = client.get(f"{row[0]}").json()
        #ao["title"] = row[2]
        # Get dates
        resource_dates = ao.get("dates")
        #pprint(ao)

        for date in resource_dates:
            date["begin"] = row[1]
            #date["label"] = "creation"
            #date["expression"] = row[1]

            #if row[2]:
                #date["end"] = row[2]

            #if row[3]:
                #date["certainty"] = "approximate"

            #if row[4]:
                #date["date_type"] = row[4]


        # Post updates
        updated = client.post(ao['uri'], json=ao)

        if updated.status_code != 200:
            print("Archival object {} update failed".format(ao['uri']))

    # Hang up
    client.session.close()
