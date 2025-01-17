import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    children = ""

    #position_num = 0

    #add_to = client.get(f'/repositories/4/archival_objects/381741/accept_children').json()
    for row in reader:
        children = children + row[0]
        move_ao = client.post('/repositories/4/archival_objects/381741/accept_children',
                          params={"children": [row[0]],
                                  "position": 41}).json()
        print(move_ao)
    #position_num += 1






