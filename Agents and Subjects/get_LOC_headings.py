# import libraries
from pprint import pprint

import requests
import csv
import os

# Set file of names to search
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\search_names.csv")

# Set destination file
csv_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\loc_matches.csv")


with open(csv_output,'w', newline='', encoding="utf-8") as csvout:
    writer = csv.writer(csvout)
    headerRow = {"Search Name", "LOC Name", "LOC URI"}
    writer.writerow(headerRow)

    with open(archival_object_csv,'r', encoding="utf-8") as csvin:
        reader = csv.reader(csvin)

        # Establish search terms
        for row in reader:
            toSearch = row[0]
            #toSearch = row[0]

            # Run search using the suggest feature
            # SEE IF YOU CAN MAKE THIS LESS BROAD - MATCH THE STRING WHEN YOU ADD
            url = f'https://id.loc.gov/authorities/names/suggest2?q={toSearch}'

            response_json = requests.get(url).json()

            hits = response_json.get("hits")

            for item in hits:
                name = item.get("aLabel")
                xmlURI = item.get("uri")

                # Write results to output csv file
                row = [row[0], name, xmlURI]

                writer.writerow(row)