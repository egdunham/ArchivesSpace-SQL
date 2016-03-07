select distinct accession.id, accession.title, accession.content_description, 
accession.identifier, extent.number, repository.name, deaccession.scope_id, 
date.expression, date.begin, date.end, user_defined.text_2, user_defined.text_4

from accession

right join extent 
	on accession.id = extent.accession_id

	left join archivesspace.deaccession
	on accession.id = deaccession.accession_id
	
	left join archivesspace.user_defined
	on accession.id = user_defined.accession_id

	left join archivesspace.repository
	on accession.repo_id = repository.id

	left join archivesspace.date
	on accession.id = date.accession_id

	left join event_link_rlshp /* one to many */
		on accession.id = event_link_rlshp.accession_id

	where not exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id = '313'
						or event.event_type_id = '1514'
						or event.event_type_id = '1515'
						or event.event_type_id = '1512'))

	and extent.extent_type_id = 278

	and (user_defined.text_2 is null
		or user_defined.text_2 != 'INV_AAO')

	and (user_defined.text_4 is null
		or user_defined.text_4 != 'INV_AAO')

	and (deaccession.scope_id is null 
		or deaccession.scope_id = '923')
