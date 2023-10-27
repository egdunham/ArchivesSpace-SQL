import os
from pprint import pprint

import asnake.utils

# Define ancestors if not using whole collection
ANCESTORS = {"/repositories/2/archival_objects/537547", "/repositories/2/archival_objects/540318",
             "/repositories/2/archival_objects/540319", "/repositories/2/archival_objects/540320",
             "/repositories/2/archival_objects/540321", "/repositories/2/archival_objects/540322",
             "/repositories/2/archival_objects/540323", "/repositories/2/archival_objects/540324",
             "/repositories/2/archival_objects/540325", "/repositories/2/archival_objects/540326",
             "/repositories/2/archival_objects/540327", "/repositories/2/archival_objects/537532",
             "/repositories/2/archival_objects/537533", "/repositories/2/archival_objects/537534",
             "/repositories/2/archival_objects/537535", "/repositories/2/archival_objects/537536",
             "/repositories/2/archival_objects/537537", "/repositories/2/archival_objects/537538",
             "/repositories/2/archival_objects/537539", "/repositories/2/archival_objects/537540",
             "/repositories/2/archival_objects/537541", "/repositories/2/archival_objects/537542",
             "/repositories/2/archival_objects/537543", "/repositories/2/archival_objects/537544"}

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/2/resources/{1244}').json()

# Walk tree and get identifiers of digital objects
for obj in asnake.utils.walk_tree(resource, client):
    instance = obj.get("instances")
    ancestors = obj.get("ancestors")

    if instance:
        for item in instance:
            sub_container = item.get("sub_container")
            top_container = sub_container.get("top_container")
            ref = top_container.get("ref")

            number = client.get(f'{ref}').json()

            #pprint(obj)

            # REM YOU NEED THE SERIES NAME/ID TO MATCH ALL THIS UP
            for ancestor in ancestors:
                #pprint(ancestor)
                if ancestor.get("ref") in ANCESTORS:
                    print(ancestor["ref"], "|", number["indicator"], "|", obj.get("ref_id"))
