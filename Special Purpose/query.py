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
    writer.writerow(["archival_object_uri", "title", "display"])

    #Open CSV reader and ignore header row
    #with open(csv_input,'r') as csvfile:
        #reader = csv.reader(csvfile)
        #next(reader, None)

        #for row in reader:
    search = "render=italic>"

    results = client.get(
        "repositories/2/search",
        params={

            "q": "title: italic",

            "page": 1,
            "page_size": 100,

            "root_record": "/repositories/2/resources/919"

        }


    ).json()
    pprint(results)

    isolateResults = results.get("results")

    for item in isolateResults:

        # Parse returned string into JSON
        individualJSON = json.loads(item.get("json"))

        #if individualJSON.get("level") == "file":
            #pprint(individualJSON["display_string"])

        # Pull out fields
        uri = individualJSON.get("uri")
        boxURI = individualJSON.get("title")

        row = [uri, boxURI, individualJSON["display_string"]]
        writer.writerow(row)



