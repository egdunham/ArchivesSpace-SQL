# Takes names from the "General" note, adds them as agent records, and deletes the note

import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Isolate the resource to be worked on
resource = client.get(f'/repositories/5/resources/{514}').json()

# Walk tree and isolate name headings in <odd> notes
for obj in asnake.utils.walk_tree(resource, client):
    notes = obj.get("notes")

    for iter in notes:
        if iter.get("type") == "odd":
            entries = iter.get("subnotes")

            for name in entries:
                startName = name.get("items")

                for i in startName:
                    updateData = obj.get("linked_agents")
                    if "Pagan, Margarita (Maria Margarita Obregón), 1934-" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/1589'}
                        updateData.append(newAgent)

                    elif "Warner, Socorro (Socorro Obregón), 1935-1992" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83351'}
                        updateData.append(newAgent)

                    elif "Obregón, Maria (Maria Gregoria Estrada), 1908-1970" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83352'}
                        updateData.append(newAgent)

                    elif "Obregón, Valentin (Valentin Flores), 1900-1967" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83353'}
                        updateData.append(newAgent)

                    elif "Estrada Porras, Jaime, 1933-" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83354'}
                        updateData.append(newAgent)

                    elif "Obregón, Mariano Flores, 1898-" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83355'}
                        updateData.append(newAgent)

                    elif "Obregón, Amalia (Amalia Nuñez), 1918-2003" in i:
                        newAgent = {'role': 'subject', 'terms': [], 'ref': '/agents/people/83356'}
                        updateData.append(newAgent)

                # Post update
                updated = client.post(obj['uri'], json=obj)

                if updated.status_code == 200:
                    print("Archival object {} updated".format(obj['uri']))
                else:
                    print(updated.json())
