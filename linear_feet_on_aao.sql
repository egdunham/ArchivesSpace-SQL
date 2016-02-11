select sum(extent.number)

from

/*Isolate all records that don't have a processing event and remove duplicates*/
(select accession.id as master_id, accession.title as title

		from accession 

		left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id
	
		left join event
			on event_link_rlshp.event_id = event.id

		where (event.event_type_id not in ('313', '1514')
			or event.event_type_id is null)

		group by accession.id, accession.title) as unprocessed

	/*Isolate records with INV_AAO */

		left join user_defined
			on unprocessed.master_id = user_defined.accession_id

		right join archivesspace.extent 
			on unprocessed.master_id = extent.accession_id

		where (text_4 = 'INV_AAO' or text_2 = 'INV_AAO')
			and extent.extent_type_id = 278
