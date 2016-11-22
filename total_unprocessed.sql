select sum(unprocessed.lf)

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

		left join collection_management on collection_management.accession_id = accession.id

			where (collection_management.processing_status_id != 257
					or collection_management.processing_status_id is null)

		)  as unprocessed

		left join archivesspace.deaccession
			on unprocessed.id = deaccession.accession_id

		left join archivesspace.user_defined
			on unprocessed.id = user_defined.accession_id
		
		/* Exclude unprocessed collection inventories on AAO */

		where ((user_defined.text_4 is null 
			or user_defined.text_4 not like 'INV_AAO')

			and (user_defined.text_2 is null 
			or user_defined.text_2 not like 'INV_AAO'))

		and (deaccession.scope_id is null 
			or deaccession.scope_id = '923')

		and (unprocessed.id <> 0 and unprocessed.id is not null)
