select 
unprocessed.accno, 
unprocessed.title,

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
unprocessed.repo_id, unprocessed.lf

from

(select
		accession.id as id, 
		accession.title as title, 
		accession.content_description as descr, 
		accession.identifier as accno, 
		accession.repo_id as repo_id, 
		extent.number as lf, 
		extent.extent_type_id as type

		from accession
	
		right join extent 
			on accession.id = extent.accession_id and extent.extent_type_id = '278'

		left join collection_management on collection_management.accession_id = accession.id

			where (collection_management.processing_status_id != 257
					or collection_management.processing_status_id is null)

		)  as unprocessed

join assessment_rlshp 
	on assessment_rlshp.accession_id = unprocessed.id

join assessment 
	on assessment_rlshp.assessment_id = assessment.id

join assessment_attribute 
	on assessment_attribute.assessment_id = assessment.id

join assessment_attribute_definition
	on assessment_attribute.assessment_attribute_definition_id = assessment_attribute_definition.id

left join archivesspace.deaccession
			on unprocessed.id = deaccession.accession_id

where (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

and (unprocessed.id <> 0 and unprocessed.id is not null)
