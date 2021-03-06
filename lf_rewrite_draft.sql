/* standardize your deacessioning or you might double-count deacessions */

/* This works, BUT some records have 313 AND 1514 and are counting twice */

select sum(number), event_type_id

from

(select distinct extent.accession_id, extent.number, event_type_id

from extent 

join accession
	on accession.id = extent.accession_id

left join event_link_rlshp
	on accession.id = event_link_rlshp.accession_id

left join event
	on event_link_rlshp.event_id = event.id

where extent.extent_type_id = 278) as foo

group by event_type_id
