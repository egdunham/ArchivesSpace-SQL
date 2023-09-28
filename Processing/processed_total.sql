select sum(processed.lf) 

from (select
		accession.id as id, 
		accession.title as title, 
		accession.content_description as descr, 
		accession.identifier as accno, 
		accession.repo_id as repo_id, 
		extent.number as lf, 
		extent.extent_type_id as type

		from accession
	
		right join extent 
			on accession.id = extent.accession_id and extent.extent_type_id = '278'

		left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id

		where exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id in ('313', '1514')))
		group by accession.id) as processed

		left join archivesspace.deaccession
			on processed.id = deaccession.accession_id

		left join archivesspace.user_defined
			on processed.id = user_defined.accession_id

		where ((user_defined.text_4 is null 
			or user_defined.text_4 not like 'INV_AAO')

			and (user_defined.text_2 is null 
			or user_defined.text_2 not like 'INV_AAO'))
		
		and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

		and (processed.id <> 0 or processed.id is not null)
