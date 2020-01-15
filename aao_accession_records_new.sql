select
	unprocessed.id, 
	unprocessed.title, 
	unprocessed.descr, 
	unprocessed.accno, 
	unprocessed.lf, 
	repository.name, 
	deaccession.scope_id, 
	date.expression, 
	date.begin, 
	date.end, 
	user_defined.text_2, 
	user_defined.text_4, 
    collection_management.processing_status_id

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
			on accession.id = extent.accession_id
			and extent.extent_type_id = '278'

		left join event_link_rlshp
			on accession.id = event_link_rlshp.accession_id

		where not exists (select 1
					from event_link_rlshp
					left join event on event_link_rlshp.event_id = event.id
					where accession.id = event_link_rlshp.accession_id 
						and (event.event_type_id in ('313', '1514')))
					) as unprocessed

		left join archivesspace.deaccession
			on unprocessed.id = deaccession.accession_id

		left join archivesspace.user_defined
			on unprocessed.id = user_defined.accession_id

		left join archivesspace.repository
			on unprocessed.repo_id = repository.id

		left join archivesspace.date
			on unprocessed.id = date.accession_id
		
        left join archivesspace.collection_management
			on unprocessed.id = collection_management.accession_id

		where (user_defined.text_2 is null
			or user_defined.text_2 NOT IN ('INV_AAO', 'Do not export'))

		and (user_defined.text_4 is null
			or user_defined.text_4 NOT IN ('INV_AAO', 'Do not export'))

		and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

group by unprocessed.id
