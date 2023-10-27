import os
from pprint import pprint

import asnake.utils

# ORIGINAL SET The 2 column CSV should look like this (without a header row):
# [ASpace ref_id],[repo_processing_note]

# archival_object_csv formatted as [refid][box][folder]
archival_object_csv = os.path.normpath("c:/users/nh48/desktop/ASpace_api_docs/notes_to_add.csv")

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Create some number of new top containers
#for i in (30, 689):
   # container_data = {"indicator": str(i),
                      #"type": "Box"}

boxes = ["294a", "294b", "294c", "294d", "319a", "369a", "374a", "376a", "380a", "467a"]
for x in boxes:
    container_data = {"indicator": x,
                       "type": "Box"}

    new_container = client.post("repositories/2/top_containers", json=container_data).json()
    #print(new_container)



    #CAN FIX TO USE STATUS CODE
    if new_container.get('error'):
        print(new_container['error'])
    else:
        print(container_data["indicator"],"|",new_container["uri"])


        #print("Box {} URI {} created".format(new_container["indicator"], new_container["uri"]))
