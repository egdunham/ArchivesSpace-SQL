import csv
import os
from pprint import pprint

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

resources = resource = client.get(f'/repositories/2/resources', params={
                    "all_ids": True,
                    "page": 1,
                    "page_size": 100,
                },).json()
result = resource.get("results")
for resource in result:
    pprint(resource.get("id_0"))