import csv
import os
from pprint import pprint

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# MERGES AGENTS SPECIFIED IN CSV

def merge(merge_input, type):

    with open(merge_input,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            result = client.post(f'/merge_requests/{type}',
                 json={
                     'uri': f'merge_requests/{type}',
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

            if result == 200:
                print("Merge successful.")

def main():
    # Set input file
    merge_input = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\subject_merge.csv")

    # Ask if merging subjects or agents
    print("\nData is expected to have a header row.\n\n")

    typeInput = input('Select an option (enter 1 or 2):\n1. Merge agents\n2. Merge subjects\n\n')

    if typeInput == "1":
        mergeType = "agent"

    else:
        mergeType = "subject"

    #VALIDATE INPUT SOMETIME

    #Pass to merge()
    merge(merge_input, mergeType)

if __name__ == "__main__":
    main()