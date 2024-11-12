import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:

        # Get AO to update
        ao = client.get(row[0]).json()
        updateInstance = ao.get("instances")

        # Create new digital object
        newObject = {
            'collection': [{'ref': '/repositories/4/resources/1054'}],
            'digital_object_id': "ms_um_mss_191_" + row[2],
            'digital_object_type': 'text',
            'file_versions': [{
                               'file_format_name': 'jpeg',
                               'file_uri': row[1] + "/acdmrn.html",
                               'is_representative': False,
                               'jsonmodel_type': 'file_version',
                               'publish': False,
                               'use_statement': 'text-data',
                               'xlink_actuate_attribute': 'onRequest',
                               'xlink_show_attribute': 'new'}],
            'is_slug_auto': False,
            'jsonmodel_type': 'digital_object',
            'level': 'image',
            'linked_instances': [{'ref': row[0]}],
            'repository': {'ref': '/repositories/4'},
            'title': 'Academic Affairs Policies and Procedures Manual'
        }

        # Create digital object and get URI
        newObject = client.post(f'/repositories/4/digital_objects', json=newObject)

        objURI = newObject.json()



        # Create a new digital object instance and attach new object
        newInstance = {'instance_type': 'digital_object',
                       'is_representative': False,
                       'jsonmodel_type': 'instance',
                       'digital_object': {'ref': objURI['uri']},
                       }

        updateInstance.append(newInstance)

        updated = client.post(ao['uri'], json=ao)

        if updated.status_code == 200:
            print("Archival object {} updated".format(ao['uri']))
        else:
            pprint(updated.json())
