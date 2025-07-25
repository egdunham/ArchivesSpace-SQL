import csv
import os
from dateutil.parser import parse
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


# Container lists
def get_container_list(repo, source):
    """
    Creates a .csv file representing all archival objects associated with a resource.
        Params: source is the URI of the guide to process. Format as /repositories/{repository id}/resources/{:id}

        Returns:
            200 if successful, error otherwise.
    """
    # Declare variables for use in writing csv
    resource = client.get(f'/repositories/{repo}/resources/{source}/ordered_records').json().get("uris")

    # Open CSV and write header row
    csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

    with open(csv_output, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Series", "URI", "Title", "Date(s)", "ID", "Box", "Folder"])

        initial_series = ""
        series = ""

        # Write records to CSV
        for item in resource:

            if item["level"] == "series":
                series = item["display_string"]

            # Works as long as file has to come after series
            elif item["level"] == "file":
                final_date = ""
                file = client.get(item["ref"]).json()
                box = ""
                folder = ""

                for date in file.get("dates"):
                    final_date = date.get("expression")

                for instance in file.get("instances"):
                    subcontainer = instance.get("sub_container")
                    folder = subcontainer.get("indicator_2")

                    topcontainer = client.get(subcontainer.get("top_container").get("ref")).json()
                    box = topcontainer.get("indicator")

                # "Series", "URI", "Title", "Date(s)", "Box", "Folder"]
                row = [series, item["ref"], file.get("title"), file.get("component_id"), final_date, box, folder]
                writer.writerow(row)

            elif item["level"] == "collection":
                continue

            else:
                initial_series = series
                series = series + "; " + item["display_string"]
                series = initial_series


# Get components
def get_ao_children(uri):
    to_get = uri + "/children"
    children = client.get(to_get).json()
    return children


#Dates
def update_ao_dates():
    """
        Updates archival object dates from .csv. Expected column order
        is [uri][label][expression][start][end][certainty][type].
        NOTE: Requires a non-blank expression field for matching.

            Returns:
                200 if successful, error otherwise.
        """
    # Read in CSV - format as [refid][label][start][end][certainty][type]
    archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input.csv")

    # Open CSV reader and ignore header row
    with open(archival_object_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            # Isolate the resource to be worked on and get dates
            to_update = client.get(f"{row[0]}").json()
            resource_dates = to_update.get("dates")

            for date in resource_dates:
                #if date["expression"] == row[2]:

                # Update by row
                if row[1] and row[1] != "":
                    date["label"] = row[1]

                if row[3] and row[3] != "":
                    date["begin"] = row[3]

                if row[4] and row[4] != "":
                    date["end"] = row[4]

                if row[5] and row[5] != "":
                    date["certainty"] = row[5]

                if row[6] and row[6] != "":
                    date["type"] = row[6]

            # Post to ASpace
            updated = client.post(to_update['uri'], json=to_update)

            if updated.status_code != 200:
                print("Archival object {} update failed".format(to_update['uri']))

# De-Excel date formatting
def format_dates(date):
    formattedDate = parse(date).strftime('%Y-%m-%d')
    return formattedDate

# Digital Objects
def create_add_digital_object(repo, guide_no, ao_ref, obj_id, uri, title, type, format):
    # Get AO to update
    ao = client.get(ao_ref).json()
    updateInstance = ao.get("instances")

    # Create new digital object
    newObject = {
        'collection': [{'ref': f'/repositories/{repo}/resources/{guide_no}'}],
        'digital_object_id': obj_id,
        'digital_object_type': type,
        'file_versions': [{
            'file_format_name': format,
            'file_uri': uri,
            'is_representative': False,
            'jsonmodel_type': 'file_version',
            'publish': False,
            'use_statement': 'text-data',
            'xlink_actuate_attribute': 'onRequest',
            'xlink_show_attribute': 'new'}],
        'is_slug_auto': False,
        'jsonmodel_type': 'digital_object',
        'level': 'image',
        'linked_instances': [{'ref': ao_ref}],
        'repository': {'ref': f'/repositories/{repo}'},
        'title': title
    }

    # Create digital object and get URI
    newObject = client.post(f'/repositories/{repo}/digital_objects', json=newObject)
    objURI = newObject.json()

    # Create a new digital object instance and attach new object
    newInstance = {'instance_type': 'digital_object',
                   'is_representative': False,
                   'jsonmodel_type': 'instance',
                   'digital_object': {'ref': objURI['uri']},
                   }

    updateInstance.append(newInstance)

    updated = client.post(ao['uri'], json=ao)

    return updated


# Utilities
def get_repo_number(name):
    if name == "Black Collections":
        return "14"
    elif name == "Chicano/a Research Collection":
        return "5"
    elif name == "Child Drama Collection" or name == "Theatre for Youth and Community":
        return "6"
    elif name == "Design and the Arts Special Collections":
        return "9"
    elif name == "Arizona Collection" or name == "Greater Arizona Collection":
        return "2"
    elif name == "Labriola National American Indian Data Center" or name == "Labriola Center":
        return "8"
    elif name == "Latin Americana Collection":
        return "12"
    elif name == "Special Collections" or name == "Rare Books and Manuscripts":
        return "3"
    elif name == "Thunderbird School of Global Management":
        return "10"
    elif name == "University Archives":
        return "4"
    elif name == "Visual Literacy Collection":
        return "7"
    else:
        return "Repository does not exist. Major bummer!"


def get_curator_by_repository(name):
    if name == "Black Collections":
        return "/agents/people/10672"
    elif name == "Chicano/a Research Collection":
        return "/agents/people/1427"
    elif name == "Child Drama Collection" or name == "Theatre for Youth and Community":
        return "/agents/people/82311"
    elif name == "Design and the Arts Special Collections":
        return "/agents/people/2171"
    elif name == "Arizona Collection" or name == "Greater Arizona Collection":
        return "/agents/people/154"
    elif name == "Labriola National American Indian Data Center" or name == "Labriola Center":
        return "/agents/people/81813"
    elif name == "Latin Americana Collection":
        return "/agents/people/10084"
    elif name == "Special Collections" or name == "Rare Books and Manuscripts":
        return "/agents/people/10084"
    elif name == "Thunderbird School of Global Management":
        return "/agents/people/2342"
    elif name == "University Archives":
        return "/agents/people/2342"
    elif name == "Visual Literacy Collection":
        return "/agents/people/1427"
    else:
        return "Curator does not exist. Major bummer!"


def create_extent(num, extentType, portion):
    extent = {
        "jsonmodel_type": "extent",
        "portion": portion,
        "number": num,
        "extent_type": extentType,
    }

    return extent


def create_event(eventType, date, user, record):
    event = {
        "jsonmodel_type": "event",
        "linked_agents": [
            {
                "ref": user,
                "role": "implementer"
            }
        ],

        "linked_records": [
            {
                "ref": record,
                "role": "source"
            }
        ],


        "date": {
            "jsonmodel_type": "date",
            "date_type": "single",
            "label": "creation",
            "begin": date,
            "era": "ce",
            "calendar": "gregorian",
            "expression": date
        },
        "event_type": eventType
    }

    return event


#format_dates("5/13/2025")