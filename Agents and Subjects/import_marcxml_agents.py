import csv
import glob
import json
import os
import pathlib
import time
from pprint import pprint

import requests

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# TODO Make command-line compatible

"""Download MARC XML from id.loc.gov

Uses record URIs to download MARC XML records from the Library of 
Congress.  Format input file as a single column of URIs with 
a header row.
"""
def download_records (input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        # Download records and populate file list - use 1 column of file names
        for row in reader:
            response = requests.get(row[0] + ".marcxml.xml")

            filename = row[0] + ".marcxml.xml"

            # You may have to correct for https as well depending
            shortname = filename.replace("https://id.loc.gov/authorities/names/", "")

            # Throws a permissions error if you try to use the filename when opening the file
            with open(f"C:\\Users\\egdunham\\Dropbox (ASU)\\__MyFiles\\Desktop\\downloaded_marc\\temp.xml",
                      'wb+') as file:
                file.write(response.content)
                importFileNames.append(filename)
                file.close()

                # This will flip its wig if you try to use the full URL as the filename
                os.rename(filepath, filepath.replace("temp.xml", str(shortname)))

        # Close CSV before moving on
        csvfile.close()

    # Establish empty file list and populate with the contents of the folder
    file_list = []
    for f in glob.iglob(directory + '/*.xml'):
        file_list.append(("files[]", open(f, "rb")))

    #Call import function
    import_records(file_list, output_file)


def import_records(file_list, output_file):
    # Import all files found
    job = json.dumps(
        {
            "job_type": "import_job",
            "job": {
                "import_type": import_type,
                "jsonmodel_type": "import_job",
                "filenames": importFileNames
            }
        }
    )

    upload = client.post("/repositories/3/jobs_with_files"
                         , files=file_list
                         , params={"job": job}).json()

    print("Import job started...")

    # Wait until the job completes before calling print functionality
    while not wait_for_completion(upload['uri']):
        print("Working ...")

    print("\nAll done! Check out " + upload['uri'] + " in ArchivesSpace.\n Now outputting results file.\n")
    print_new_records(upload['uri'], output_file)

def print_new_records(job_no, output_file):
    # Export a list of records created with their URIs
    id_set = []

    with open(output_file, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        headerRow = {"Sort Name", "Identifier"}
        writer.writerow(headerRow)

        # Get IDs of all records created in import
        payload = {'all_ids': 'true'}
        find_ids = client.get(f'{job_no}/records', params=payload).json()

        # For each record, get the link to the imported record
        for item in find_ids:
            id_set.append(item)

        # Use IDs identified to get URIs and names
        id_payload = {'id_set': id_set}
        get_records = client.get(f'{job_no}/records', params=id_payload).json()

        # Get the display name, and match against the CSV
        for record in get_records:
            item = record.get("record")
            identifier = item.get("ref")

            entity = client.get(identifier).json()

            names = entity.get("display_name")

            sort_name = names.get("sort_name")

            row = [sort_name, identifier]
            writer.writerow(row)

    csvout.close()

def wait_for_completion(job_no):
    mustend = time.time() + 600
    totimeout = 600

    while time.time() < mustend:
        totimeout = totimeout - 15

        # Poll status every 15 seconds to see if it finished; time out after 10 minutes
        status = client.get(job_no).json().get("status")

        # Return if job is finished; otherwise provide an update
        if status == "completed":
            return True
        else:
            pprint("This job is " + status + ". " + str(round(totimeout / 60)) + " minutes until timeout.")
            time.sleep(15)
            return False

"""Body of program

Get input from user to populate the normpath and input and output file names.  NOTE:
values are currently hardcoded during development.
NEED:
Input file
Output file
Output directory
Path
"""

#TODO Control for repository numbering

# Get list of MARC records to download
to_import = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\merge_input.csv")

# Set path to output file
to_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\merge_output.csv")

# Set source file for data and declare array for file names
directory = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\downloaded_marc")
filepath = "C:\\Users\\egdunham\\Dropbox (ASU)\\__MyFiles\\Desktop\\downloaded_marc\\temp.xml"

pathlib.Path(directory).mkdir(exist_ok=True)
importFileNames = []

# Declare import type
import_type = "marcxml_auth_agent"

# Call functions to handle various tasks
download_records(to_import, to_output)
