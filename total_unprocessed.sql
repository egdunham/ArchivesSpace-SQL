select sum(extent.number)

from archivesspace.accession right join archivesspace.extent 
	on accession.id = extent.accession_id

	left join archivesspace.collection_management
	on accession.id = collection_management.accession_id
	
	left join archivesspace.user_defined
	on accession.id = user_defined.accession_id

	where extent.extent_type_id = 278
	and (collection_management.processing_status_id is null 
		or collection_management.processing_status_id != 257)

	and (user_defined.text_2 is null
		or user_defined.text_2 != 'INV_AAO')

	and (user_defined.text_4 is null
		or user_defined.text_4 != 'INV_AAO')
