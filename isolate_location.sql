left join instance on accession.id = instance.accession_id

left join sub_container
	on sub_container.instance_id = instance.id

left join top_container_link_rlshp
	on top_container_link_rlshp.sub_container_id = sub_container.id

left join top_container
	on top_container_link_rlshp.top_container_id = top_container.id

left join top_container_housed_at_rlshp
	on top_container.id = top_container_housed_at_rlshp.top_container_id
    
left join location
	on top_container_housed_at_rlshp.location_id = location.id
