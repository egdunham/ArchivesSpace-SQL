import csv
import os
from pprint import pprint

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Read in CSV - format as [refid][container uri]
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\renumber_csv.csv")

#Open CSV reader and ignore header row
with open(archival_object_csv,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        refid = row[0]

        # Isolate the resource to be worked on using find_by_id
        url = 'repositories/2/find_by_id/archival_objects?ref_id[]=' + refid
        ao = client.get(url).json()
        # get archival object as json
        ao_ref = ao.get("archival_objects")[0].get("ref")
        ao = client.get(ao_ref).json()

        #Isolate top container
        instance = ao.get("instances")

        for item in instance:
            sub_container = item.get("sub_container")
            top_container = sub_container.get("top_container")
            ref = top_container.get("ref")

            # Link to updated top container
            top_container["ref"] = row[1]

            #pprint(ao_ref)

            updated = client.post(ao_ref, json=ao)

            if updated.status_code == 200:
                print("Archival object {} updated".format(ao['uri']))
            else:
                print(updated.json())
