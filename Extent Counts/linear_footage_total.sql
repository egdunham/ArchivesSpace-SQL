select sum(extent.number)

from accession

left join archivesspace.extent
on accession.id = extent.accession_id

left join archivesspace.deaccession
on accession.id = deaccession.accession_id

-- Add linear feet
join enumeration_value on enumeration_value.id = extent.extent_type_id
where enumeration_value.value like "%linear%"

and (deaccession.scope_id is null or deaccession.scope_id = '923')