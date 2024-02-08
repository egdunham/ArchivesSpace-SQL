from pprint import pprint

import asnake.utils
import os
import csv

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

merge_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\orphan_people.csv")

# Read in CSV - format as [refid][container uri]
name_check = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\name_check.csv")

with (open(merge_output, 'w', newline='') as csvout):
    writer = csv.writer(csvout)
    headerRow = {"ASpace ID", "ASpace Display"}
    writer.writerow(headerRow)

    # Isolate the resource to be worked on
    with open(name_check,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            refid = row[0]
            item = client.get(refid).json()



            if len(item.get("agent_contacts")) == 0 and len(item.get("related_agents")) == 0 and len(item.get("agent_record_identifiers")) == 0:
                agent = client.get(refid).json().get("display_name").get("sort_name")

                clean_agent = agent.encode('utf-8').decode('ascii', 'ignore')
                row = [row[0], clean_agent]
                writer.writerow(row)

