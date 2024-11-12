import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")
archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

with open(csv_output,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write CSV header row
    writer.writerow(["uri", "item ID", "refid", "title", "date", "notes", "physdesc", "subjects", "agents"])

    #Open CSV reader and ignore header row
    with open(archival_object_csv,'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            dates = ""
            noteContent = ""
            noteSingleContent = ""
            subjects = "$"
            agents = "$"
            itemID = ""

            resource = client.get(f'/{row[0]}').json()

            if resource.get("component_id"):
                itemID = resource.get("component_id")

            # Get dates
            if resource["dates"]:
                for date in resource.get("dates"):
                    itemDate = date.get("expression")
                    dates = itemDate

            # Get any associated notes
            if resource.get("notes"):
                notes = resource.get("notes")

                for note in notes:
                    noteSingleContent = note.get("content")
                    noteID = note.get("persistent_id")

                    if note.get("subnotes"):
                        subnote = note.get("subnotes")

                        for item in subnote:
                            noteContent = item.get("content")

            # Get linked agents
            if resource.get("linked_agents"):
                agentArray = resource.get("linked_agents")
                for agent in agentArray:
                    role = agent.get("role")
                    subject = agent.get("ref")
                    agentName1 = client.get(subject).json()
                    agentName = agentName1.get("title")
                    agents = agents + "||" + agentName + "|" + role

            # Get subjects
            if resource.get("subjects"):
                subjectArray = resource.get("subjects")

                for subject in subjectArray:
                    ref = subject.get("ref")
                    toAdd = client.get(ref).json()
                    subjectName = toAdd.get("title")
                    subjectSource = toAdd.get("source")
                    subjects = subjects + "||" + subjectName + "|" + subjectSource

            row = [row[0], itemID, resource.get("refid"), resource.get("title"), dates, noteContent, noteSingleContent, subjects, agents]
            writer.writerow(row)