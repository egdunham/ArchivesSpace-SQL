select sum(archivesspace.extent.number)

from archivesspace.accession
right join archivesspace.extent on accession.id = extent.accession_id

join archivesspace.deaccession
on accession.id = deaccession.accession_id

where extent.extent_type_id = 278
