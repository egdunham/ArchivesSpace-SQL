import csv
import os
from pprint import pprint
import asnake
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["uri", "barcode"])

    with open(archival_object_csv,'r', encoding='utf-8-sig') as csvin:
        reader = csv.reader(csvin)
        next(reader, None)

        # Establish search terms
        for row in reader:
            container = client.get(row[0]).json()
            row = [row[0], container.get("barcode")]
            writer.writerow(row)