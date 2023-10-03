import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

PHOTOGRAPHERS = ["/agents/people/5642", "/agents/people/5663", "/agents/people/5641", "/agents/people/5630",
                 "/agents/people/5675", "/agents/people/5653", "/agents/people/8129", "/agents/people/5650",
                 "/agents/people/5664", "/agents/people/5683", "/agents/people/5672", "/agents/people/5679",
                 "/agents/people/5660", "/agents/people/5645", "/agents/people/83060", "/agents/people/5631",
                 "/agents/people/10493", "/agents/people/5661", "/agents/people/5680", "/agents/people/5677",
                 "/agents/people/5668", "/agents/people/5632", "/agents/people/5633", "/agents/people/5659",
                 "/agents/people/5606", "/agents/people/5667", "/agents/people/5665", "/agents/people/5657",
                 "/agents/people/5644", "/agents/people/5655", "/agents/people/5662", "/agents/people/5149",
                 "/agents/people/5647", "/agents/people/5676", "/agents/people/5654", "/agents/people/5646",
                 "/agents/people/5656", "/agents/people/5666", "/agents/people/5673", "/agents/people/5658",
                 "/agents/people/5648", "/agents/people/5674", "/agents/people/5682"]

# Isolate the resource to be worked on
resource = client.get(f'/repositories/2/resources/{637}').json()

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