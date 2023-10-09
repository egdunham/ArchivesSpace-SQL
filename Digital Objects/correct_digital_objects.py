import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#agent people, corporate_entities

# Isolate the resource to be worked on
resource = client.get(f'/repositories/5/resources/{514}').json()

# Walk tree and get identifiers of digital objects
for obj in asnake.utils.walk_tree(resource, client):
    instance = obj.get("instances")

    for item in instance:

        # Retrieve digital object(s) using provided URIs
        dig_obj_ref = item.get("digital_object")["ref"]
        dig_obj = client.get(f'{dig_obj_ref}').json()

        # Reformat identifier and replace
        identifier = dig_obj.get("file_versions")[1]["file_uri"].replace("http://www.asu.edu/lib/archives/digital-collections/AZSI/full/", "")
        new_identifier = identifier.replace(".JPG", "")
        dig_obj["digital_object_id"] = new_identifier

        # Remove ", Digital Object" from title

        title = dig_obj["title"]

        dig_obj["title"] = title.replace(", Digital Object", "")

        #print(dig_obj)

        # Update using digital object URI
        updated = client.post(dig_obj['uri'], json=dig_obj)

        if updated.status_code == 200:
            print("Digital object {} updated".format(dig_obj['uri']))
        else:
            print(updated.json())

