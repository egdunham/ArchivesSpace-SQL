import csv
import os

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:

        # Isolate the resource to be worked on
        resource = client.get(f'{row[0]}').json()
        agents = resource.get("linked_agents")

        # Loop through list of agents attached to an archival object
        for agent in agents:
            if agent.get("relator") is None:

                if agent.get("ref") == row[1]:
                    agent["relator"] = row[2]

                    # Post update
                    updated = client.post(resource['uri'], json=resource)

                    if updated.status_code != 200:
                        print(updated.json())


# Hang up
client.session.close()