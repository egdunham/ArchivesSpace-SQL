import csv

import asnake.utils
import os

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Read in CSV - format as [refid][expression][start]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\date_update.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        refid = row[0]

        # Isolate the resource to be worked on using find_by_id

        ao = client.get(refid).json()

        # Get dates
        resource_dates = ao.get("dates")

        for date in resource_dates:
            date["begin"] = row[2]
            date["expression"] = row[1]


        # Post updates
        updated = client.post(ao['uri'], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao['uri']))
        else:
            print(updated.json())

    # Hang up
    client.session.close()
