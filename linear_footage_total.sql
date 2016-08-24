select sum(extent.number)

from archivesspace.accession

right join archivesspace.extent
on archivesspace.accession.id = archivesspace.extent.accession_id

left join archivesspace.deaccession
			on unprocessed.id = deaccession.accession_id

where extent.extent_type_id = 278

and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')
