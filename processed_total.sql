select sum(processed.lf) 

from (select distinct
		accession.id as id, 
		accession.title as title, 
		accession.content_description as descr, 
		accession.identifier as accno, 
		accession.repo_id as repo_id, 
		extent.number as lf, 
		extent.extent_type_id as type

		from accession
	
		right join extent 
			on accession.id = extent.accession_id

		left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id

		where exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id in ('313', '1514')))) as processed

		left join archivesspace.deaccession
			on processed.id = deaccession.accession_id

		where processed.type = 278
		
		and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')
