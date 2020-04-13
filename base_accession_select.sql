 select
    accession.id,
    repository.name,
    accession.title,
    accession.content_description,
    MAX(IF(enumeration_value.value like '%Box%', extent.number, NULL)) as boxes, 
    MAX(IF(date.date_type_id = 905, date.expression, NULL)) as date,
    MAX(IF(date.date_type_id = 905, date.begin, NULL)) as date_begin,
    MAX(IF(date.date_type_id = 905, date.end, NULL)) as date_end,
    MAX(IF(user_defined.text_2 like '%INV_AAO%' or user_defined.text_4 like '%INV_AAO%', "TRUE", "FALSE")) as on_aao,
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
	
    group by accession.id, user_defined.text_2, user_defined.text_4, deaccessioned
