import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#agent people, corporate_entities

agent_set = client.get(f'/agents/people/7389').json()

print(agent_set["used_within_published_repositories"])

