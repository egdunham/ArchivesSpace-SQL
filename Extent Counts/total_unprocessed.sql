select sum(extent.number)

-- Includes materials with inventories on AAO and totally unprocessed materials

from (select distinct
		accession.id as id, 
		accession.title as title, 
		accession.content_description as descr, 
		accession.identifier as accno, 
		accession.repo_id as repo_id 
		
        from accession
        
		where not exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
                    left join enumeration_value on enumeration_value.id = event.event_type_id
					where accession.id = event_link_rlshp.accession_id 
						and (enumeration_value.value = "processed"))
		) as unprocessed
        
        -- Add linear feet
        join extent on unprocessed.id = extent.accession_id
        join enumeration_value on enumeration_value.id = extent.extent_type_id

        -- Remove deaccessioned collections
        left join archivesspace.deaccession
		on unprocessed.id = deaccession.accession_id
        
		where enumeration_value.value like "%linear%"
        and (deaccession.scope_id is null or deaccession.scope_id = '923')