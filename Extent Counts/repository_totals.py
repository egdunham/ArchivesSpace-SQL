import json
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set global variables for tally
processedLF = 0
unprocessedLF = 0
aaoLF = 0

resourceSet = client.get(f'/repositories/4/accessions?all_ids=true').json()

for id in resourceSet:

    accession = client.get(f'/repositories/4/accessions/{id}').json()

    # Set variables for determining AAO vs. totally unprocessed and linear feet to add
    isProcessed = False
    noCount = False
    aaoBycollMan = False
    aaoByUserField = False
    toAdd = 0

    # Determine if deaccessioned in full and break
    if accession.get("deaccessions"):
        for item in accession.get("deaccessions"):
            if item["scope"] == "whole":
                break

    #Pull A/V validation records
    if accession.get("id_1") and "A/V" in accession["id_1"]:
        noCount = True

    # Get Linear Feet
    if accession.get("extents"):
        extents = accession.get("extents")

        for extent in extents:
            if extent["extent_type"] == "linear_feet" and noCount is False:
                toAdd = float(extent["number"])

    # Determine processed, unprocessed, or on AAO
    if accession.get("collection_management"):
        processed = accession.get("collection_management")

        if processed.get("processing_status"):

            if processed["processing_status"] == "completed":
                isProcessed = True
                processedLF = processedLF + toAdd

            elif processed["processing_status"] == "Inventory on AAO":
                aaoBycollMan = True

    if accession.get("user_defined"):
        userDef = accession.get("user_defined")

        if userDef.get("text_2") and userDef["text_2"] == "INV_AAO":
            aaoByUserField = True

        elif userDef.get("text_4") and userDef["text_4"] == "INV_AAO":
            aaoByUserField = True

    if aaoBycollMan is True or aaoByUserField is True:
        aaoLF = aaoLF + toAdd

    elif isProcessed is False and noCount is False:
        unprocessedLF = unprocessedLF + toAdd

print("Linear Feet Processed:", processedLF)
print("Linear Feet Unprocessed:", unprocessedLF)
print("Linear Feet on AAO:", aaoLF)
