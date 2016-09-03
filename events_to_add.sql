select accession.id, accession.identifier, accession.repo_id, accession.title, processing_status_id, event_type_id

from accession 

left join extent 
	on accession.id = extent.accession_id and extent_type_id = 278

join collection_management on accession.id = collection_management.accession_id

left join event_link_rlshp
		on accession.id = event_link_rlshp.accession_id

left join event on event_link_rlshp.event_id = event.id

where not exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id = '313'
						or event.event_type_id = '1514'
						or event.event_type_id = '1515'
						or event.event_type_id = '1512'))



and processing_status_id = 257

order by repo_id, title
