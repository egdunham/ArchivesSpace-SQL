/* You can also search for the event types  */

select 
	accession.id,
	repository.name,
	accession.title,
	event_type_id, 
	date.begin, 
	extent.extent_type_id,
	extent.number

from accession

	join extent 
			on accession.id = extent.accession_id and extent_type_id = 278

	left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id 

	left join event
		on event_link_rlshp.event_id = event.id and event.event_type_id in ('313','1514')

	left join date
		on date.event_id = event.id

	join repository on accession.repo_id = repository.id

	where date.begin between '2015-07-01' and '2016-06-30'

group by accession.id
