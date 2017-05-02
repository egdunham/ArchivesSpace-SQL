select accession.id, repository.name, accession.identifier, accession.title, 
accession.content_description,
accession.condition_description, 
accession.general_note, 
accession.access_restrictions_note, 
MAX(IF(enumeration_value.id = '1348', extent.number, NULL)) as audio_recordings, 			
MAX(IF(enumeration_value.id = '1370', extent.number, NULL)) as boxes, 	
MAX(IF(enumeration_value.id = '1366', extent.number, NULL)) as disks, 
MAX(IF(enumeration_value.id = '1349', extent.number, NULL)) as filmstrips, 
MAX(IF(enumeration_value.id = '1354', extent.number, NULL)) as microfiche, 
MAX(IF(enumeration_value.id = '1355', extent.number, NULL)) as microfilm, 
MAX(IF(enumeration_value.id = '1350', extent.number, NULL)) as motion_picture_film, 
MAX(IF(enumeration_value.id = '1301', extent.number, NULL)) as photographs, 
MAX(IF(enumeration_value.id = '278', extent.number, NULL)) as linear_feet, 
MAX(IF(enumeration_value.id = '280', extent.number, NULL)) as photo_prints, 
MAX(IF(enumeration_value.id = '281', extent.number, NULL)) as photo_slides, 
MAX(IF(enumeration_value.id = '282', extent.number, NULL)) as reels, 
MAX(IF(enumeration_value.id = '1611', extent.number, NULL)) as vhs, 
MAX(IF(enumeration_value.id = '1351', extent.number, NULL)) as videotapes, 
location.title

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

	left join collection_management on accession.id = collection_management.accession_id

	where (collection_management.processing_status_id != 257
		or collection_management.processing_status_id is null)

group by accession.id
