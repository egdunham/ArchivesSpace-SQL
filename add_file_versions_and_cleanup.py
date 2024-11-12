import csv
import os
from pprint import pprint

import asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set file of names to search
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University\Desktop\loc_matches.csv")

with open(archival_object_csv, 'r', encoding="utf-8") as csvin:
    reader = csv.reader(csvin)

    # Establish search terms
    for row in reader:
        # Isolate the resource to be worked on
        resource = client.get(row[0]).json()
        fileUpdate = resource.get("file_versions")

        # Set level and type
        resource["level"] = "image"
        resource["digital_object_type"] = "still_image"

        # Add file versions
        newThumb = {'is_representative': False, 'jsonmodel_type': 'file_version', 'use_statement': 'image-thumbnail', 'file_uri' : row[1], 'xlink_actuate_attribute' : 'onLoad'}
        fileUpdate.append(newThumb)

        newFull = {'is_representative': False, 'jsonmodel_type': 'file_version', 'use_statement': 'image-service', 'file_uri' : row[2], 'xlink_actuate_attribute' : 'onRequest'}
        fileUpdate.append(newFull)

        #pprint(resource)

        updated = client.post(row[0], json=resource)

        if updated.status_code == 200:
            print("Archival object {} updated".format(row[0]))
        else:
            print(updated.json())