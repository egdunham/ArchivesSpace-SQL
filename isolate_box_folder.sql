select archival_object.id, archival_object.position, top_container.indicator, sub_container.indicator_2, archival_object.title

from archival_object

left join instance
	on archival_object.id = instance.archival_object_id

left join container
	on instance.id = container.instance_id

left join sub_container
	on sub_container.instance_id = instance.id

left join top_container_link_rlshp
	on top_container_link_rlshp.sub_container_id = sub_container.id

left join top_container
	on top_container_link_rlshp.top_container_id = top_container.id

where root_record_id = 436
