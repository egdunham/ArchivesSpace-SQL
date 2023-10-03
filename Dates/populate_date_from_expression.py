import asnake.utils
import re

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()


def month_replace(exp):
    to_replace = None

    if " January " in exp:
        to_replace = exp.replace(" January ", "-01-")

    if " February " in exp:
        to_replace = exp.replace(" February ", "-02-")

    if " March " in exp:
        to_replace = exp.replace(" March ", "-03-")

    if " April " in exp:
        to_replace = exp.replace(" April ", "-04-")

    if " May " in exp:
        to_replace = exp.replace(" May ", "-05-")

    if " June " in exp:
        to_replace = exp.replace(" June ", "-06-")

    if " July " in exp:
        to_replace = exp.replace(" July ", "-07-")

    if " August " in exp:
        to_replace = exp.replace(" August ", "-08-")

    if " September " in exp:
        to_replace = exp.replace(" September ", "-09-")

    if " October " in exp:
        to_replace = exp.replace(" October ", "-10-")

    if " November " in exp:
        to_replace = exp.replace(" November ", "-11-")

    if " December " in exp:
        to_replace = exp.replace(" December ", "-12-")

    return to_replace


# Isolate the resource to be worked on
resource = client.get(f'/repositories/2/resources/{637}').json()

# Walk tree and use expression value as start value
for obj in asnake.utils.walk_tree(resource, client):
    resource_dates = obj.get("dates")

    # Loop over date fields
    for date in resource_dates:
        start = date.get("begin")
        expression = date.get("expression")
        date_type = date.get("date_type")
        certainty = date.get("certainty")
        replace_value = date.get("expression")

        # Ignore "Undated"
        if expression is not None and date_type == "single" and start is None and expression != "Undated":
            monthRegex = re.compile(r'[A-Z]')
            dayRegex = re.compile(r'-\d$')

            # For circa, strip the circa and set type to approximate
            if "circa " in replace_value:
                replace_value = date["expression"].replace("circa ", "")
                date["certainty"] = "approximate"

            if monthRegex.search(replace_value):
                replace_value = month_replace(replace_value)

            if dayRegex.search(replace_value):
                # Define character to replace
                ch = '-'

                # Break string into component characters
                lst1 = list(replace_value)
                lst2 = list(ch)

                # Replace second occurrence only
                for i in lst2:
                    sub_string = i
                    val = -1
                    for i in range(0, 2):
                        val = replace_value.find(sub_string, val + 1)
                    lst1[val] = "-0"

                # Update replacement value and flag update as true
                replace_value = ''.join(lst1)

            # Update begin string
            date["begin"] = replace_value

            # Post updates
            updated = client.post(obj['uri'], json=obj)

            if updated.status_code == 200:
                print("Archival object {} updated".format(obj['uri']))
            else:
                print(updated.json())

# Hang up
client.session.close()
