select sum(extent.number)

from archivesspace.accession
right join archivesspace.extent
on archivesspace.accession.id = archivesspace.extent.accession_id

where extent.extent_type_id = 278
