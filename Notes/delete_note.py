import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/5/resources/{514}').json()

for obj in asnake.utils.walk_tree(resource, client):
    notes = obj.get("notes")

    for iter in notes:
        if iter.get("type") == "odd":
            notes.remove(iter)

            # Post update
            updated = client.post(obj['uri'], json=obj)

            if updated.status_code == 200:
                print("Archival object {} updated".format(obj['uri']))
            else:
                print(updated.json())