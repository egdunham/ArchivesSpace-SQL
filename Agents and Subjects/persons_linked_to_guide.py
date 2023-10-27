import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/2/resources/{1235}').json()

# Walk tree and print display name and URI of associated agent
for resource in asnake.utils.walk_tree(resource, client):
    resource_agents = resource.get("linked_agents")

    for agent in resource_agents:
        print_agent = client.get(agent["ref"]).json().get("names")

        for obj in print_agent:
            if obj.get("is_display_name"):
                name = obj.get("sort_name")
                print(name + " | " + agent["ref"])
