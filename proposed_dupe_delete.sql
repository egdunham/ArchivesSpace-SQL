select * 

from event_link_rlshp

where event_link_rlshp.event_id not in
	(select * from 
    (select min(event.id)
	from event
		group by 
			lock_version, json_schema_version, suppressed, repo_id, event_type_id, 
			outcome_id, outcome_note, timestamp, created_by, last_modified_by, 
			create_time, system_mtime, user_mtime) as nondupe)
