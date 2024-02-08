import csv
import os
from pprint import pprint

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

"""Match names

Reads names from a CSV file formatted as [Search Name][LOC URI].  If a match is found, writes the name, the LOC 
URI, and the ASpace URI to the output file.
"""

# Get list of MARC records to download
search_criteria = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\search_criteria.csv")

# Set path to output file
search_results = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\search_results.csv")

# Define list of names to search - use [Search name][LOC URI]
with open(search_criteria,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    # Define CSV output file - use [LOC URI][LOC Name][ASpace ref][ASpace Name]
    with open(search_results, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        headerRow = {"Search ID", "Search Name", "Existing ID", "Existing Name"}
        writer.writerow(headerRow)

        for row in reader:

            # Get IDs of all records created in import
            # Replace type to search for different types of headings - endpoint is generic search
            payload = {'page': '1', 'q': row[0], 'type': ['agent_person']}
            job = client.get(f'/repositories/3/search', params=payload).json()

            compare = row[0]
            results = job.get("results")
            hits = job.get("total_hits")

            if hits != 0:
                for hit in results:

                    ref = hit.get("id")
                    name = hit.get("title")


                    if name == compare and ref != row[2]:

                        row = [row[2], compare, ref, name]

                        writer.writerow(row)