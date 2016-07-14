SELECT 
  accession.id, repository.name, accession.title, 
  MAX(IF(enumeration_value.value like '%Box%', extent.number, NULL)) as boxes, 
	MAX(IF(enumeration_value.value like '%linear%', extent.number, NULL)) as feet, 
	MAX(IF(event.event_type_id in ('313', '1514'), 'Processed', NULL)) as status, 
	accession.identifier as accno, resource.identifier, user_defined.text_2, 
	user_defined.text_4, location.title

from accession

	left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id

	left join event on event_link_rlshp.event_id = event.id

	left join extent 
		on accession.id = extent.accession_id
	
	left join enumeration_value 
		on extent.extent_type_id = enumeration_value.id

	left join repository
		on accession.repo_id = repository.id

	left join spawned_rlshp
		on accession.id = spawned_rlshp.accession_id

	left join resource on resource.id = spawned_rlshp.resource_id

	left join user_defined
			on accession.id = user_defined.accession_id

	left join archivesspace.instance 
		on accession.id = instance.accession_id

	left join archivesspace.container 
		on instance.id = container.instance_id

	left join archivesspace.housed_at_rlshp 
		on container.id = housed_at_rlshp.container_id

	left join archivesspace.location 
		on location.id = housed_at_rlshp.location_id

	where location.title not like '%RSB%'

group by accession.id
