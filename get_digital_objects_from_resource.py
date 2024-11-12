import csv
import os
from pprint import pprint

import asnake.utils
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/4/resources/{466}').json()

# Set destination file
csv_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\loc_matches.csv")


with open(csv_output,'w', newline='', encoding="utf-8") as csvout:
    writer = csv.writer(csvout)
    headerRow = {"ID", "Digital Object ID"}
    writer.writerow(headerRow)

    # Walk tree and get identifiers of digital objects
    for obj in asnake.utils.walk_tree(resource, client):
        instance = obj.get("instances")

        for item in instance:

            # Retrieve digital object(s) using provided URIs
            if item.get("digital_object") is not None:
                dig_obj_ref = item.get("digital_object")["ref"]
                dig_obj = client.get(f'{dig_obj_ref}').json()

                # Reformat identifier and replace
                identifier = dig_obj.get("digital_object_id")
                uri = dig_obj.get("uri")

                #print(identifier, uri)

                row = [identifier, uri]
                writer.writerow(row)
