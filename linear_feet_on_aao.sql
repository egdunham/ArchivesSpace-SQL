/* Update to use events */
select sum(extent.number)

from archivesspace.accession 
right join archivesspace.extent 
on archivesspace.accession.id = archivesspace.extent.accession_id

left join archivesspace.user_defined 
on archivesspace.accession.id = archivesspace.user_defined.accession_id

left join archivesspace.collection_management
on archivesspace.accession.id = archivesspace.collection_management.accession_id

where (text_4 = 'INV_AAO' or text_2 = 'INV_AAO')
and extent.extent_type_id = 278
and processing_status_id is null
