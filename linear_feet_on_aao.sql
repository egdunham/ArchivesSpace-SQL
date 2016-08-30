select sum(extent.number)

from accession

	left join user_defined
		on accession.id = user_defined.accession_id

	right join archivesspace.extent 
		on accession.id = extent.accession_id and extent.extent_type_id = 278

		left join archivesspace.deaccession
			on accession.id = deaccession.accession_id

	where (text_4 = 'INV_AAO' or text_2 = 'INV_AAO')

		and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

		and (accession.id <> 0 and accession.id is not null)
