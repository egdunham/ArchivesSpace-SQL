select sum(extent.number), repository.name

from archivesspace.accession

join archivesspace.extent 
	on accession.id = extent.accession_id and extent_type_id = 278

left join archivesspace.user_defined 
	on accession.id = user_defined.accession_id

left join archivesspace.instance 
	on accession.id = instance.accession_id

left join archivesspace.container 
	on instance.id = container.instance_id

left join archivesspace.housed_at_rlshp 
	on container.id = housed_at_rlshp.container_id

left join archivesspace.location 
	on location.id = housed_at_rlshp.location_id

left join archivesspace.deaccession
	on accession.id = deaccession.accession_id

left join archivesspace.repository
	on accession.repo_id = repository.id

where  
(location.title like '%RSB%' or location.title is null)

and (user_defined.text_2 like '%RSB%' or user_defined.text_2 is null)

and (user_defined.text_4 like '%RSB%' or user_defined.text_4 is null)


and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

		and (accession.id <> 0 and accession.id is not null)

group by repository.name
