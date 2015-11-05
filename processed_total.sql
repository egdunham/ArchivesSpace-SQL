select sum(archivesspace.extent.number)

from archivesspace.accession
right join archivesspace.extent on accession.id = extent.accession_id

left join archivesspace.collection_management
on accession.id = collection_management.accession_id

where collection_management.processing_status_id = 257 
	and extent.extent_type_id = 278
