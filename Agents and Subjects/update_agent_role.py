import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

PHOTOGRAPHERS = ["/agents/people/6039", "/agents/people/1901", "/agents/people/4601", "/agents/people/6030"]

# Isolate the resource to be worked on
resource = client.get(f'/repositories/4/resources/{656}').json()

# Walk tree and print display name and URI of associated agent
for obj in asnake.utils.walk_tree(resource, client):

    agents = obj.get("linked_agents")

    # Loop through list of agents attached to an archival object
    for agent in agents:
        if agent.get("relator") is None:

            if agent.get("ref") in PHOTOGRAPHERS:
                agent["relator"] = "Photographer"
                agent["role"] = "creator"

                # Post update
                updated = client.post(obj['uri'], json=obj)

                if updated.status_code == 200:
                    print("Archival object {} updated".format(obj['uri']))
                else:
                    print(updated.json())

# Hang up
client.session.close()