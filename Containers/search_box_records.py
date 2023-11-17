import csv
import os

import asnake.utils


# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#Set destination
csv_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\csv_output.csv")

# Isolate the resource to be worked on
resource = client.get(f'/repositories/4/resources/{1054}').json()


with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # write CSV header row
    writer.writerow(["date", "num"])

    # Walk tree and isolate name headings in <odd> notes
    for obj in asnake.utils.walk_tree(resource, client):
        date = obj.get("dates")
        instance = obj.get("instances")

        for exp in date:
            expression = exp.get("expression")


        for container in instance:
            subcontainer = container.get("sub_container")

            for top in subcontainer:
                topcontainer = subcontainer.get("top_container")
                ref = topcontainer.get("ref")

                box = client.get(ref).json()
                num = box.get("indicator")

                row = [expression, num]

                # Write row to file
                writer.writerow(row)


