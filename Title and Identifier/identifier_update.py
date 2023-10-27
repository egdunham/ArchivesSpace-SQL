import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/2/resources/{451}').json()

# Walk tree
for obj in asnake.utils.walk_tree(resource, client):

    if obj.get("component_id") is not None:
        identifier = obj.get("component_id").replace("<_emph>", '')
        obj["component_id"] = identifier

        # Post updates
        updated = client.post(obj['uri'], json=obj)

        if updated.status_code == 200:
            print("Archival object {} updated".format(obj['uri']))
        else:
            print(updated.json())

# Hang up
client.session.close()