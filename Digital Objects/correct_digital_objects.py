import asnake.utils

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

#agent people, corporate_entities

# Isolate the resource to be worked on
resource = client.get(f'/repositories/4/resources/{1347}').json()

# Walk tree and get identifiers of digital objects
for obj in asnake.utils.walk_tree(resource, client):
    instance = obj.get("instances")

    for item in instance:

        # Retrieve digital object(s) using provided URIs
        if item.get("digital_object") is not None:
            dig_obj_ref = item.get("digital_object")["ref"]
            dig_obj = client.get(f'{dig_obj_ref}').json()

            # Reformat identifier and replace
            identifier = dig_obj.get("digital_object_id")
            new_identifier = "UP_ASUA_" + identifier
            dig_obj["digital_object_id"] = new_identifier

            # Set level and type
            dig_obj["level"] = "image"
            dig_obj["digital_object_type"] = "still_image"

            # Set use statement and format
            file_version = dig_obj.get("file_versions")
            for version in file_version:

                version["file_format_name"] = "jpeg"

                if version["xlink_actuate_attribute"] == "onRequest":
                    version["use_statement"] = "image-service"

                if version["xlink_actuate_attribute"] == "onLoad":
                    version["use_statement"] = "image-thumbnail"


            #print(dig_obj)

            updated = client.post(dig_obj['uri'], json=dig_obj)

            if updated.status_code == 200:
                print("Archival object {} updated".format(dig_obj['uri']))
            else:
                print(updated.json())
