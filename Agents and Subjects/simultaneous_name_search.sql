select agent_person.id, resource.repo_id, accession.repo_id, agent_family_id, 
agent_corporate_entity_id, linked_agents_rlshp.accession_id, archival_object_id, event_id, resource_id, primary_name

from linked_agents_rlshp

left join agent_person on linked_agents_rlshp.agent_person_id = agent_person.id

left join name_person on name_person.agent_person_id = agent_person.id

left join resource on linked_agents_rlshp.resource_id = resource.id

left join accession on linked_agents_rlshp.accession_id = accession.id

where agent_person.id = 416
