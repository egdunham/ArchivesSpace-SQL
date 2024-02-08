import csv
import os
from pprint import pprint

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# MERGES AGENTS SPECIFIED IN CSV

# Set input file
merge_input = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\agent_merge.csv")

with open(merge_input,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        result = client.post('/merge_requests/agent',
             json={
                 'uri': 'merge_requests/agent',
                 'target': {
                     'ref': row[0]
                 },
                 'victims': [
                     {
                         'ref': row[1]
                     }
                 ]
             }
             )

        print(result)
