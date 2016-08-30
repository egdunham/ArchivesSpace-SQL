select accession.id

from accession

right join archivesspace.extent
on accession.id = extent.accession_id and extent.extent_type_id = 278

left join archivesspace.deaccession
			on accession.id = deaccession.accession_id

where (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

and (accession.id <> 0 and accession.id is not null)
