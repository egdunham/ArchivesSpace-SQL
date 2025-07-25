import csv
import os
from pprint import pprint

import ASUtil

# Authenticate via asnake
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# Set destination
csv_input = os.path.normpath(r"C:\Users\egdunham\Desktop\input.csv")

# Define functions for use in accession record construction
#TODO determine if duplicate name matching is reacting to differences in the whole object or only name. May require more sophisticated searching
def create_donor_person():
    # TODO Add ability to use matched name
    # Search for name and return URI as donor_uri if extant

    donor = {
        'jsonmodel_type': 'agent_person',
        'is_slug_auto': True,
        'names': [
            {
                'jsonmodel_type': 'name_person',
                'authorized': True,
                'is_display_name': True,
                'sort_name_auto_generate': True,
                'primary_name': row[61],
                'name_order': 'direct',
            }
        ],
        'agent_contacts': [],
    }

    contact = {
        'name': row[61],
        'address_1': row[45],
        'address_2': row[46],
        "address_3": row[47],
        'city': row[48],
        'region': row[49],
        'email': row[50],
        'is_representative': False,
        'jsonmodel_type': 'agent_contact',
        'post_code': row[53],
        'telephones': [],
    }

    if row[56]:
        phone = {
            'jsonmodel_type': 'telephone',
            'number': row[56],
            'number_type': 'home'
        }
        contact["telephones"].append(phone)

    donor["agent_contacts"].append(contact)

    # Create new donor and return URI
    new_donor = client.post(f'/agents/people', json=donor)
    donor_uri = ""

    if new_donor.status_code != 200 and new_donor.json().get("error").get("conflicting_record"):
        print("Donor (Person) could not be created: ")
        records = new_donor.json().get("error").get("conflicting_record")
        donor_uri = handle_conflicting_names(records)
        return donor_uri

    elif new_donor.status_code == 200:
        donor_uri = new_donor.json().get("uri")
        return donor_uri

    else:
        print("Well, that's really unexpected! Error is:\n")
        pprint(new_donor.json())
        return -1


def create_donor_corporate():
    donor = {
        'jsonmodel_type': 'agent_corporate_entity',
        'agent_contacts': [],
        'names': [
            {
                'jsonmodel_type': 'name_corporate_entity',
                'primary_name': row[61],
                'conference_meeting': False,
                'rules': row[62],
                'sort_name_auto_generate': True,
            }
        ],
        'publish': True,
    }

    # Create and append corporate contact
    contact = {
        'jsonmodel_type': 'agent_contact',
        'name': row[52],
        'address_1': row[45],
        'address_2': row[46],
        'address_3': row[47],
        'city': row[48],
        'region': row[49],
        'email': row[50],
        'post_code': row[53],
        'telephones': [],
    }

    # Add phone number if included
    if row[56]:
        phone = {
            'jsonmodel_type': 'telephone',
            'number': row[56],
            'number_type': 'business'
        }
        contact["telephones"].append(phone)

    # Add contact to donor record
    donor["agent_contacts"].append(contact)

    new_donor = client.post(f'/agents/corporate_entities', json=donor)
    donor_uri = ""

    if new_donor.status_code != 200 and new_donor.json().get("error").get("conflicting_record"):
        print("Donor (Corporate) could not be created: ")
        records = new_donor.json().get("error").get("conflicting_record")
        donor_uri = handle_conflicting_names(records)
        return donor_uri

    elif new_donor.status_code == 200:
        donor_uri = new_donor.json().get("uri")
        return donor_uri

    else:
        print("Well, that's really unexpected! Error is:\n")
        pprint(new_donor.json())
        return -1

# TODO check to see if this works if an error isn't thrown on creation of the accession, in which case it doesn't
# If the donor could not be created because a conflicting record exists, ask user
# if the coflicting record should be used instead.
def handle_conflicting_names(records):
    i = 1
    for record in records:
        name = client.get(record).json()
        dispName = name.get("display_name").get("primary_name")
        pprint(str(i) + ": " + dispName)
        i = i + 1

    toUse = input("Enter the number corresponding to the matching record you would like to use: ")
    toReturn = ""
    j = 1
    for record in records:
        if str(j) == toUse:
            toReturn = record
            break

        else:
            j = j + 1

    return toReturn

# Add a digital object if needed
# MAY NEED TO PASS REPO EXPLICITLY
def create_digital_object():
    # Format start date
    start_date = ASUtil.format_dates(row[5])

    # Handle restriction types
    if row[72] == "Yes":
        restriction_type = "allow"

    elif row[72] == "No":
        restriction_type = "disallow"

    else:
        restriction_type = "conditional"

    # Handle type translations
    if row[69] == "Cartographic":
        digobj_type = "cartographic"

    elif row[69] == "Mixed Materials":
        digobj_type = "mixed_materials"

    elif row[69] == "Moving Image":
        digobj_type = "moving_image"

    elif row[69] == "Notated Music":
        digobj_type = "notated_music"

    elif row[69] == "Software, Multimedia":
        digobj_type = "software_multimedia"

    elif row[69] == "Sound Recording":
        digobj_type = "sound_recording"

    elif row[69] == "Sound Recording (Musical)":
        digobj_type = "sound_recording_musical"

    elif row[69] == "Sound Recording (Non-musical)":
        digobj_type = "sound_recording_nonmusical"

    elif row[69] == "Still Image":
        digobj_type = "still_image"

    elif row[69] == "Text":
        digobj_type = "text"

    else:
        digobj_type = "mixed_materials"

    # Create new object
    newObject = {
        'digital_object_id': row[2] + "_0" + row[3],
        'digital_object_type': digobj_type,
        'file_versions': [{
            'file_uri': row[75],
            'is_representative': False,
            'jsonmodel_type': 'file_version',
            'publish': False,
            'use_statement': 'text-data',
            'xlink_actuate_attribute': 'onRequest',
            'xlink_show_attribute': 'new'}],
        'rights_statements': [],
        'is_slug_auto': False,
        'jsonmodel_type': 'digital_object',
        'level': 'image',
        'repository': {'ref': f'/repositories/{repo}'},
        'title': row[1]
    }

    # Create new rights statement
    new_rights_stmt = {
        'jsonmodel_type': 'rights_statement',
        'other_rights_basis': 'donor',
        'rights_type': 'other',
        'start_date': start_date,
        'acts': [],
        'notes': [],
    }

    # Handle information about whether something can go on the Repository
    new_act = {
        'act_type': 'disseminate',
        'jsonmodel_type': 'rights_statement_act',
        'restriction': restriction_type,
        'start_date': start_date,
        'notes': [],
    }

    # Add explanation of "other" response if needed
    if row[73]:
        new_statement = {
            'content': ["Can materials be put on repository?: " + row[73]],
            'jsonmodel_type': 'note_rights_statement_act',
            'publish': False,
            'type': 'additional_information'
        }
        new_act["notes"].append(new_statement)
        new_rights_stmt["acts"].append(new_act)

    if row[76]:
        content = "Rights Transferred: " + row[76]
        if row[74]:
            content = content + "; Rights Statement: " + row[74]

        new_note = {
            'content': [content],
            'jsonmodel_type': 'note_rights_statement',
            'publish': False,
            'type': 'additional_information'
        }

        new_rights_stmt["notes"].append(new_note)

    # Append new rights statement to new object
    newObject["rights_statements"].append(new_rights_stmt)

    # Create digital object and get URI
    newObject = client.post(f'/repositories/{repo}/digital_objects', json=newObject)
    objURI = newObject.json()
    return objURI


# Open CSV reader and ignore header row
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:

        # Assign proper repository number and curator
        repo = ASUtil.get_repo_number(row[0])
        curator = ASUtil.get_curator_by_repository(row[0])

        # Reformat accession date if needed
        accession_date = ""

        if "/" in row[5]:
            accession_date = ASUtil.format_dates(row[5])

        else:
            accession_date = row[5]

        # Build accession record
        accession = {
            'jsonmodel_type': 'accession',
            'acquisition_type': row[8].lower(),

            'is_slug_auto': True,

            'accession_date': accession_date,

            # Add agent array
            'linked_agents': [],

            # Add title and content
            'title': row[1],
            'content_description': row[10],

            # Add accession number
            'id_0': row[2],
            'id_1': "0" + row[3],

            # Add arrays for later use
            'extents': [],
            'dates': [],
            'linked_events': [],
            'instances': [],
        }

        # Create dates and append
        if row[16]:
            newDate = {
                'calendar': 'gregorian',
                'date_type': row[19],
                'era': 'ce',
                'expression': row[16],
                'jsonmodel_type': 'date',
                'label': 'Creation',
            }
            accession["dates"].append(newDate)

        # Create extents and append
        if row[26]:
            boxes = {
                    'jsonmodel_type': 'extent',
                    'portion': 'whole',
                    'number': row[26],
                    'extent_type': 'Box(es)',
                }
            accession["extents"].append(boxes)

        if row[27]:
            linear_feet = {
                    'jsonmodel_type': 'extent',
                    'portion': 'whole',
                    'number': row[27],
                    'extent_type': 'linear_feet',
                }
            accession["extents"].append(linear_feet)

        # Create donor object
        if row[44] == "agent_person" and row[61] != "Unknown":
            donorURI = create_donor_person()
            donor = {
                'is_primary': False,
                'ref': donorURI,
                'relator': 'Donor',
                'role': 'Source',
                'terms': []
            }

            if donorURI:
                accession["linked_agents"].append(donor)

        elif row[44] == "agent_corporate_entity" and row[61] != "Unknown":
            donorURI = create_donor_corporate()
            donor = {
                'is_primary': False,
                'ref': donorURI,
                'relator': 'Donor',
                'role': 'Source',
                'terms': []
            }
            if donorURI:
                accession["linked_agents"].append(donor)

        # Create additional extents and append
        if row[28] and row[29]:
            accession["extents"].append(ASUtil.create_extent(row[28], row[29], "part"))

        if row[30] and row[31]:
            accession["extents"].append(ASUtil.create_extent(row[30], row[31], "part"))

        if row[32] and row[33]:
            accession["extents"].append(ASUtil.create_extent(row[32], row[33], "part"))

        if row[34] and row[35]:
            accession["extents"].append(ASUtil.create_extent(row[34], row[35], "part"))

        # TODO add back use restrictions
        # Add access restrictions if applicable
        if row[6] == "1":
            restrictions = {'access_restrictions': True, }
            restriction_note = {'access_restrictions_note': row[6], }
            accession.update(restrictions)
            accession.update(restriction_note)

        # Create processing note and append
        if row[82] or row[83]:
            processingText = ""
            if row[83] and row[83]:
                processingText = row[83] + " " + row[82]

            elif row[82]:
                processingText = row[82]

            else:
                processingText = row[83]

            accession.update(
                {'collection_management':
                    {
                        'jsonmodel_type': 'collection_management',
                        'processing_plan': processingText
                    }
                }
            )

        # Create loose item note and append
        if row[38]:
            accession.update(
                {'user_defined':
                    {
                        'jsonmodel_type': 'user_defined',
                        'text_3': row[38]
                    }
                }
            )

        # TODO Handle Protocols

        # Create and append a digital object
        if row[69]:
            new_uri = create_digital_object()
            newInstance = {'instance_type': 'digital_object',
                           'is_representative': False,
                           'jsonmodel_type': 'instance',
                           'digital_object': {'ref': new_uri["uri"]},
                           }

        # Post final accession
        newInstance = client.post(f'repositories/{repo}/accessions', json=accession)
        instanceID = newInstance.json().get("uri")
        accession["instances"].append(instanceID)

        if newInstance.status_code == 200:
            print("Accession " + instanceID + " created.")

        else:
            print("Accession could not be created: ")
            pprint(newInstance.json())

        # Create deed signed event
        if row[41] != "":
            signDate = ""

            if "/" in row[41]:
                signDate = ASUtil.format_dates(row[41])

            else:
                signDate = row[41]

            event = ASUtil.create_event("agreement_signed", signDate, curator, instanceID)
            newEvent = client.post(f'repositories/{repo}/events', json=event)
            eventNo = newEvent.json().get("uri")
            accession["linked_events"].append(eventNo)

            if newEvent.status_code != 200:
                print("Event could not be created: ")
                pprint(newEvent.json())

        # Add assessment using new accession record URI
        deed = False
        if row[41]:
            deed = True

        # Format survey begin date if needed
        surveyDate = ""
        if "/" in row[5]:
            surveyDate = ASUtil.format_dates(row[5])

        else:
            surveyDate = row[5]

        assessment = {
            "jsonmodel_type": "assessment",
            "records": [
                {
                    "ref": instanceID
                }
            ],
            "surveyed_by": [
                {
                    "ref": "/agents/people/1"
                }
            ],

            'ratings': [{'definition_id': 1,
                         'global': True,
                         'label': 'Reformatting Readiness',
                         'readonly': False},
                        {'definition_id': 2,
                         'global': True,
                         'label': 'Housing Quality',
                         'readonly': False},
                        {'definition_id': 3,
                         'global': True,
                         'label': 'Physical Condition',
                         'readonly': False},
                        {'definition_id': 4,
                         'global': True,
                         'label': 'Physical Access (arrangement)',
                         'readonly': False},
                        {'definition_id': 5,
                         'global': True,
                         'label': 'Intellectual Access (description)',
                         'readonly': False},
                        {'definition_id': 6,
                         'global': True,
                         'label': 'Interest',
                         'readonly': False,
                         'value': row[36]},
                        {'definition_id': 7,
                         'global': True,
                         'label': 'Documentation Quality',
                         'readonly': False},
                        {'definition_id': 8,
                         'global': True,
                         'label': 'Research Value',
                         'readonly': True,
                         'value': row[36]}],

            'deed_of_gift': deed,
            "survey_begin": surveyDate,
            "review_required": False,
        }

        newAssessment = client.post(f'repositories/{repo}/assessments', json=assessment)
        assessmentID = newAssessment.json().get("uri")

        if newAssessment.status_code != 200:
            print("Event could not be created: ")
            pprint(newAssessment.json())
