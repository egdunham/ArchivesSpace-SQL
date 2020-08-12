select * 
	
    from(select
    accession.identifier as accno,
    accession.title,
    (CASE WHEN assessment_attribute_definition.label='Housing Quality'
            then assessment_attribute.value
            ELSE NULL 
        END) as housing,
        
        (CASE WHEN assessment_attribute_definition.label='Physical Condition'
            then assessment_attribute.value
            ELSE NULL 
        END) as physicalcondition,
        
        (CASE WHEN assessment_attribute_definition.label='Physical Access (arrangement)'
            then assessment_attribute.value
            ELSE NULL 
        END) as arrangement,
        
        (CASE WHEN assessment_attribute_definition.label='Research Value'
            then assessment_attribute.value
            ELSE NULL 
        END) as value,
        
        repository.name,
        MAX(IF(enumeration_value.value like '%linear%', extent.number, NULL)) as lf, 
        accession.content_description as descr,
        
        MAX(IF(user_defined.text_2 like '%INV_AAO%' or user_defined.text_4 like '%INV_AAO%', "TRUE", "FALSE")) as on_aao,
        collection_management.processing_plan,
    accession.id,
    MAX(IF(event.event_type_id = 313, "TRUE", "FALSE")) as processed_1,
    MAX(IF(event.event_type_id = 1514, "TRUE", "FALSE")) as processed_2,
    MAX(IF(date.date_type_id = 905, date.expression, NULL)) as date,
    MAX(IF(date.date_type_id = 905, date.begin, NULL)) as begin,
    MAX(IF(date.date_type_id = 905, date.end, NULL)) as end,
    
    MAX(IF(user_defined.text_2 like '%Do not export%' or user_defined.text_4 like '%Do not export%', "TRUE", "FALSE")) as no_publish,
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
        
	left join collection_management
		on accession.id = collection_management.accession_id
        
        left join assessment_rlshp 
	on assessment_rlshp.accession_id = accession.id

left join assessment 
	on assessment_rlshp.assessment_id = assessment.id

left join assessment_attribute 
	on assessment_attribute.assessment_id = assessment.id

left join assessment_attribute_definition
	on assessment_attribute.assessment_attribute_definition_id = assessment_attribute_definition.id
	
    group by accession.id, user_defined.text_2, user_defined.text_4, deaccessioned, collection_management.processing_plan, assessment_attribute.value, assessment_attribute_definition.label) as filter_values
    
    where filter_values.name not in ("Thunderbird School of Global Management")

    and filter_values.deaccessioned = "FALSE"
    and filter_values.processed_1 = "FALSE"
    and filter_values.processed_2 = "FALSE"
    and filter_values.no_publish = "FALSE"
	and filter_values.title != "Audio-Visual Validation Record"
