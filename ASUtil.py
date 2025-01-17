import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

def get_container_list(source):
    """
    Creates a .csv file representing all archival objects associated with a resource.
        Params: source is the URI of the guide to process. Format as /repositories/{repository id}/resources/{:id}

        Returns:
            200 if successful, error otherwise.
    """
    # Declare variables for use in writing csv
    series = "None"
    top_level = source

    # Get the root of the resource record's tree
    uri = source + "/tree/root"
    resource = client.get(uri).json()
    waypoints = resource.get("precomputed_waypoints").get("").get("0")
    pprint(waypoints)
    # CLOSE - CAN'T KEEP OPENING AND CLOSING THE DOCUMENT

    for waypoint in waypoints:
        stop = False
        series = waypoint["title"]

        # Check to see if the items in the next level down are at "file" or "item" level
        if waypoint["child_count"] != 0:

            while stop is False:

                first_waypoint = get_waypoints(top_level, waypoint)
                to_check = first_waypoint.get("precomputed_waypoints").get(waypoint["uri"]).get("0")

                #print(first_waypoint)
                if to_check[0]["child_count"] != 0:
                    backup = series
                    #print(to_check[0])
                    for item in to_check:
                        # Add subseries to series
                        series = series + "; " + item["title"]
                        #print(series)
                        first_waypoint = get_waypoints(top_level, item)
                        to_check = first_waypoint.get("precomputed_waypoints").get(item["uri"]).get("0")

                        if to_check[0]["child_count"] != 0:
                            print("Not Implemented beyond subseries")
                            stop = True

                        else:
                            write_basic_container_list(to_check, series)
                            series = backup
                            stop = True

                else:
                    #print("HERE")
                    list_base = get_ao_children(waypoint["uri"])
                    write_basic_container_list(to_check, series)
                    #3write_basic_container_list(list_base)
                    #stop = True
                    top_level = source
                    stop = True

        # Otherwise, work through the container list
        else:
            print("HERE1")
            #list_base = get_ao_children(waypoint["uri"])
            #write_basic_container_list(list_base)


def get_waypoints(uri, waypoint):
    to_get = uri + "/tree/node"
    node_info = client.get(to_get, params={
        "node_uri": waypoint["uri"],
    }).json()
    return node_info


def write_basic_container_list(list_base, series):

    # Add box and folder
    csv_output = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/csv_output.csv")

    with open(csv_output, 'a', newline='') as csvfile:
        add_header = True
        writer = csv.writer(csvfile)
        if add_header == True:
            writer.writerow(["uri", "series", "item ID", "title", "startDate", "endDate", "dateExpression", "dateType", "box", "folder"])
            add_header = False

        for item in list_base:
            itemID = ""
            startDate = ""
            endDate = ""
            dateExpression = ""
            dateType = ""
            box = ""
            folder = ""

            #print(item)

            if item.get("component_id"):
                itemID = item.get("component_id")

            # Get dates
            if item.get("dates"):
                for date in item.get("dates"):
                    dateExpression = date.get("expression")
                    startDate = date.get("begin")
                    endDate = date.get("end")
                    dateType = date.get("type")

            if item.get("containers"):
                for container in item.get("containers"):
                    box = container.get("top_container_indicator")
                    folder = container.get("indicator_2")

            row = [item["uri"], series, itemID, item.get("title"), startDate, endDate, dateExpression, dateType, box, folder]
            writer.writerow(row)


def get_ao_children(uri):
    to_get = uri + "/children"
    children = client.get(to_get).json()
    return children

def update_ao_dates():
    """
        Updates archival object dates from .csv. Expected column order
        is [uri][label][expression][start][end][certainty][type].
        NOTE: Requires a non-blank expression field for matching.

            Returns:
                200 if successful, error otherwise.
        """
    # Read in CSV - format as [refid][label][start][end][certainty][type]
    archival_object_csv = os.path.normpath(r"C:\Users\egdunham\OneDrive - Arizona State University/Desktop/input1.csv")

    # Open CSV reader and ignore header row
    with open(archival_object_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            # Isolate the resource to be worked on and get dates
            to_update = client.get(f"{row[0]}").json()
            resource_dates = to_update.get("dates")

            for date in resource_dates:
                if date["expression"] == row[2]:

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


#create_add_digital_object(2, 919, "/repositories/2/archival_objects/1262202",
                          #"ms_cm_mss_409_20170829202550",
                         #"https://wayback.archive-it.org/8125/20170829202550/https://www.facebook.com/johnmccain/",
                          #"John McCain Facebook Page", "text", "HTML")