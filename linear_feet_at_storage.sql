select sum(extent.number), accession.repo_id

from archivesspace.accession
join archivesspace.extent on accession.id = extent.accession_id and extent_type_id = 278
left join archivesspace.user_defined on accession.id = user_defined.accession_id
left join archivesspace.instance on accession.id = instance.accession_id
left join archivesspace.container on instance.id = container.instance_id
left join archivesspace.housed_at_rlshp on container.id = housed_at_rlshp.container_id
left join archivesspace.location on location.id = housed_at_rlshp.location_id

where (location.title like '%RSB%'
or user_defined.text_2 = 'RSB'
or user_defined.text_4 = 'RSB')

group by repo_id
