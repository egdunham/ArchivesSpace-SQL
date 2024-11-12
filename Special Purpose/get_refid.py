import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


# Set file of names to search
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["uri", "refid"])

    #Open CSV reader and ignore header row
    with open(archival_object_csv,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            id = row[0]
            ao = client.get(f"{id}").json()
            refid = ao.get("ref_id")

            row = [row[0], refid]
            writer.writerow(row)