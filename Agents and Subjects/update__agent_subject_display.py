import csv
import glob
import json
import os
import pathlib
from pprint import pprint

import requests
# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


def format_name(merge_input):
    with (open(merge_input, 'r') as csvfile):
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:

            aspace_name = client.get(row[1]).json()

            display = aspace_name.get("display_name")
            display["sort_name_auto_generate"] = False
            display["sort_name"] = row[0]

            # Post updates
            updated = client.post(row[1], json=aspace_name)

            if updated.status_code == 200:
                print("Archival object {} updated".format(row[1]))
            else:
                print(updated.json())

    csvfile.close()


def format_subject(merge_input):
    with (open(merge_input, 'r') as csvfile):
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:

            result = client.get(row[0]).json()

            # Update Authority ID
            result["authority_id"] = row[2]

            # Update Terms
            terms = result.get("terms")

            for item in terms:
                item["term"] = row[1]

            # Update Title
            result["title"] = row[1]

            # Post updates
            updated = client.post(row[0], json=result)

            if updated.status_code == 200:
                print("Archival object {} updated".format(row[0]))
            else:
                print(updated.json())

    csvfile.close()

def main():
    file_name = input("Enter name of input file.  Files must be formatted as CSV.\n\n")

    # Set input file
    merge_input = os.path.normpath(f"C:\\Users\\egdunham\\Dropbox (ASU)\\__MyFiles\\Desktop\\{file_name}")

    typeInput = input('Select an option (enter 1 or 2):\n1. Update agents\n2. Update subjects\n\n')

    if typeInput == "1":
        print("Expected column headings are [sort_name][ref]\n\n")
        callAgent = input("Continue? (Y/N)\n\n")

        if callAgent == "Y":
            format_name(merge_input)

        elif callAgent == "N":
            main()

        else:
            print("\n\nInvalid input.  Enter Y to continue or N to return to the main menu.")

    elif typeInput == "2":
        print("Expected column headings are [ref][title][authority_id]\nWill not work with multi-term updates.")
        callSubject = input("Continue? (Y/N)\n\n")

        if callSubject == "Y":
            format_subject(merge_input)

        elif callSubject == "N":
            main()

        else:
            print("\n\nInvalid input.")
            main()


# Run main
if __name__ == "__main__":
    main()
