select sum(extent.number)

from resource

	join repository 
		on resource.repo_id = repository.id

	left join extent 
		on resource.id = extent.resource_id and extent.extent_type_id = '278'

	where exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where resource.id = event_link_rlshp.resource_id 
						and (event.event_type_id in ('313', '1514')))


	and repository.name like '%Thunderbird%'
