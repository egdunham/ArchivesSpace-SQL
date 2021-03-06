select * 
	
    from(select
    accession.id,
    repository.name,
    accession.title,
    accession.content_description as descr,
    MAX(IF(enumeration_value.value like '%linear%', extent.number, NULL)) as lf, 
    MAX(IF(event.event_type_id = 313, "TRUE", "FALSE")) as processed_1,
    MAX(IF(event.event_type_id = 1514, "TRUE", "FALSE")) as processed_2,
    MAX(IF(date.date_type_id = 905, date.expression, NULL)) as date,
    MAX(IF(date.date_type_id = 905, date.begin, NULL)) as begin,
    MAX(IF(date.date_type_id = 905, date.end, NULL)) as end,
    MAX(IF(user_defined.text_2 like '%INV_AAO%' or user_defined.text_4 like '%INV_AAO%', "TRUE", "FALSE")) as on_aao,
    MAX(IF(user_defined.text_2 like '%Do not export%' or user_defined.text_4 like '%Do not export%', "TRUE", "FALSE")) as no_publish,
	accession.identifier as accno,
    user_defined.text_2, 
	user_defined.text_4,
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
		on accession.id = date.accession_id
	
    group by accession.id, user_defined.text_2, user_defined.text_4, deaccessioned) as filter_values
    
    where filter_values.name not in ("Thunderbird School of Global Management", "Architecture & Environmental Design Library")
    
	and filter_values.on_aao = "FALSE"
    and filter_values.deaccessioned = "FALSE"
    and filter_values.processed_1 = "FALSE"
    and filter_values.processed_2 = "FALSE"
    and filter_values.no_publish = "FALSE"
	and filter_values.title != "Audio-Visual Validation Record"
