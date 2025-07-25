import csv
import os
from pprint import pprint

import ASUtil

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")
repo = 2
guide = 919

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        new_ao = {
            'jsonmodel_type': 'archival_object',
            'publish': False,
            'dates': [
                {'expression': row[1],
                 'begin': row[2],
                 'date_type': 'single',
                 'label': 'creation',
                 'jsonmodel_type': 'date'}],
            'notes': [],
            'level': 'file',
            'title': row[0],
            'parent': {'ref': f'/repositories/{repo}/archival_objects/1263521'},
            'resource': {'ref': f'/repositories/{repo}/resources/{guide}'}
        }

        physdesc = {'content': [row[4]], 'jsonmodel_type': 'note_singlepart', 'publish': False, 'type': 'physdesc'}
        new_ao["notes"].append(physdesc)

        newInstance = client.post(f'repositories/{repo}/archival_objects', json=new_ao)
        instanceID = newInstance.json().get("uri")

        if newInstance.status_code == 200:
            print("Archival object {} created".format(instanceID))
            print("Creating digital object ...")
            new_digobj = ASUtil.create_add_digital_object(2, 919, f'{instanceID}',
                                                          "ms_cm_mss_409_" + f'{row[5]}',
                                                          f'{row[3]}',
                                                          f'{row[0]}', "text", "HTML")
            if new_digobj.status_code == 200:
                print("New digital object created successfully!\n")

            else:
                print("Digital object could not be created.\n")
                print(new_digobj.json())

        else:
            print("Major bummer! Something went wrong.\n")
            pprint(newInstance.json())