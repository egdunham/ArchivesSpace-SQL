import csv
import os
from pprint import pprint

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Need to add instances and then update them

# Read in CSV - format as [refid][container uri]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV files
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        refid = row[0]
        topContainer = row[1]
        ao = client.get(refid).json()
        pprint(ao)
        updateInstance = ao.get("instances")

        # Add new instance with top container
        newInstance = {'instance_type': 'mixed_materials',
                       'is_representative': False,
                       'jsonmodel_type': 'instance',
                       'sub_container': {'jsonmodel_type': 'sub_container',
                                         'top_container': {'jsonmodel_type': 'top_container',
                                                           'ref': row[1]}}
                       }

        updateInstance.append(newInstance)

        updated = client.post(ao['uri'], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao['uri']))
        else:
            pprint(updated.json())