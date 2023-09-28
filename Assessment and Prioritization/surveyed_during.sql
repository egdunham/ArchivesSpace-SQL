select sum(extent.number)

from accession

left join extent 
	on accession.id = extent.accession_id and extent_type_id = 278

join assessment_rlshp
	on accession.id = assessment_rlshp.accession_id
    
join assessment
	on assessment.id = assessment_rlshp.assessment_id
    
where assessment.survey_begin between '2018-01-01' and '2018-12-31'
