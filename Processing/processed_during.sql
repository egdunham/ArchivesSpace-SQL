/* You can also search for the event types  */

select * 
	
    from(select
    accession.id,
    repository.name,
    accession.title,
    MAX(IF(enumeration_value.value like '%linear%', extent.number, NULL)) as lf, 
    MAX(IF(event.event_type_id = 313, "TRUE", "FALSE")) as processed_1,
    MAX(IF(event.event_type_id = 1514, "TRUE", "FALSE")) as processed_2,
    date.begin as start_date,
    date.end as end_date,
	accession.identifier as accno,
    IF(deaccession.scope_id = 922, "TRUE", "FALSE") as deaccessioned	
	
    from accession

	left join event_link_rlshp
		on accession.id = event_link_rlshp.accession_id

	left join event on event_link_rlshp.event_id = event.id

	left join extent
		on accession.id = extent.accession_id
	
	left join enumeration_value 
		on extent.extent_type_id = enumeration_value.id

	left join repository
		on accession.repo_id = repository.id
	
    left join user_defined
		on accession.id = user_defined.accession_id
	
    left join archivesspace.deaccession
		on accession.id = deaccession.accession_id
	
    left join archivesspace.date
		on event.id = date.event_id
	
    group by accession.id, date.begin, date.end, deaccessioned) as filter_values
    
    where (processed_1 = "TRUE" or processed_2 = "TRUE") and start_date between '2020-01-01' and '2020-12-30'
