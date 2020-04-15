select filter_values.name, sum(filter_values.lf)
	
    from(select
    accession.id,
    repository.name as name,
    MAX(IF(enumeration_value.value like '%linear%', extent.number, NULL)) as lf, 
    MAX(IF(event.event_type_id = 313, "TRUE", "FALSE")) as processed_1,
    MAX(IF(event.event_type_id = 1514, "TRUE", "FALSE")) as processed_2,
    MAX(IF(user_defined.text_2 like '%INV_AAO%' or user_defined.text_4 like '%INV_AAO%', "TRUE", "FALSE")) as on_aao

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

	group by accession.id, name
    ) as filter_values

where filter_values.processed_1 = "FALSE"
and filter_values.processed_2 = "FALSE"
and filter_values.on_aao = "FALSE"

group by name, processed_1, processed_2, on_aao
