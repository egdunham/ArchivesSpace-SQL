import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Read in CSV - format as [refid][container uri]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\csv_input.csv")

# Isolate the resource to be worked on
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        refid = row[0]
        item = client.get(refid).json()
        agents = item.get("linked_agents")
        agentRef = row[1]

        # Add new agent to list
        newAgent = {'role': 'creator', 'relator': 'Photographer', 'terms': [], 'ref': agentRef}
        agents.append(newAgent)

        # Post update
        updated = client.post(item['uri'], json=item)

        if updated.status_code == 200:
            print("Archival object {} updated".format(item['uri']))
        else:
            print(updated.json())

        #pprint(agents)