import csv
import os
from pprint import pprint

import asnake.utils
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        refid = row[0]
        ao = client.get(refid).json()

        # Replace "Tape "
        component = ao.get("component_id")
        update_component = component.replace("Tape ", "")
        updateInstance = ao.get("instances")

        # Create new container and clear component_id
        container_data = {'jsonmodel_type': 'top_container',
                          'indicator': update_component,
                          'type': 'Tape',
                          'barcode': row[1]}

        new_container = client.post("repositories/4/top_containers", json=container_data).json()
        ao["component_id"] = ""

        # Create and append new instance
        newInstance = {'instance_type': 'moving_images',
                       'is_representative': False,
                       'jsonmodel_type': 'instance',
                       'sub_container': {'jsonmodel_type': 'sub_container',
                                         'top_container': {'jsonmodel_type': 'top_container',
                                                           'ref': new_container.get("uri")}}
                       }

        updateInstance.append(newInstance)

        updated = client.post(ao['uri'], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao['uri']))
        else:
            pprint(updated.json())
