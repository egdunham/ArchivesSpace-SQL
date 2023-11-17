import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#agents can be: people, corporate_entities

agent_set = client.get(f'/agents/corporate_entities/9600').json()

print(agent_set["used_within_published_repositories"])

