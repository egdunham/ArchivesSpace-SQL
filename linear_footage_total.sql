select accession.id

from accession

right join archivesspace.extent
on accession.id = extent.accession_id

left join archivesspace.deaccession
			on accession.id = deaccession.accession_id

where extent.extent_type_id = 278

and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

and (accession.id <> 0 and accession.id is not null)
