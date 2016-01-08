
/* Mostly works - need to figure out how to display processing date and do a date range */

select distinct accession.id, accession.title, accession.content_description, 
accession.identifier, extent.number

from accession

	right join extent 
	on accession.id = extent.accession_id

	left join archivesspace.deaccession
	on accession.id = deaccession.accession_id

	left join event_link_rlshp /* one to many */
		on accession.id = event_link_rlshp.accession_id



	where exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					left join date on date.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id = '313'
						or event.event_type_id = '1514')
					 and date.begin like '%2015%')

	and extent.extent_type_id = 278

	and (deaccession.scope_id is null 
		or deaccession.scope_id = '923')
