import os
import csv
from pprint import pprint

import asnake.utils


# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

merge_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\names.csv")

# Isolate the resource to be worked on /repositories/:repo_id/jobs/active
payload = {'all_ids': True}
ao = client.get(f'/agents/people', params = payload).json()

with open(merge_output, 'w', newline='') as csvout:
    writer = csv.writer(csvout)
    headerRow = {"ASpace ID", "ASpace Display", "Imported"}
    writer.writerow(headerRow)

    for id in ao:
        agent = client.get(f'/agents/people/{id}').json().get("display_name").get("sort_name")
        record_control = False


        if len(client.get(f'/agents/people/{id}').json().get("agent_record_controls")) != 0:
            record_control = True


        clean_agent = agent.encode('utf-8').decode('ascii', 'ignore')
        row = [id, clean_agent, record_control]
        writer.writerow(row)
