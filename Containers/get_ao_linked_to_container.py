import csv
import os
from pprint import pprint
import json
import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
csv_input = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["archival_object_uri", "box", "folder"])

    #Open CSV reader and ignore header row
    with open(csv_input,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:

            results = client.get(
                "repositories/6/search",
                params={
                    "q": {f"top_container_uri_u_sstr: /repositories/6/top_containers/30760"},
                    "page": 1,
                    "page_size": 100,
                },
            ).json()

            isolateResults = results.get("results")

            for item in isolateResults:

                folderNo = ""
                boxURI = ""
                # Parse returned string into JSON
                individualJSON = json.loads(item.get("json"))

                # Pull out fields
                uri = individualJSON.get("uri")

                if individualJSON.get("instances"):
                    instances = individualJSON.get("instances")

                    for instance in instances:

                        if instance["instance_type"] == "mixed_materials":
                            #pprint(instance)
                            subcontainer = instance.get("sub_container")

                            if subcontainer.get("indicator_2"):
                                folderNo = subcontainer["indicator_2"]

                            topcontainer = subcontainer.get("top_container")
                            boxURI = topcontainer.get("ref")

                        row = [uri, boxURI, folderNo]
                        writer.writerow(row)