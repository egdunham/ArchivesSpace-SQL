select repository.name, sum(extent.number)

from archivesspace.accession right join archivesspace.extent 
	on accession.id = extent.accession_id

left join archivesspace.repository
	on accession.repo_id = repository.id

where accession.accession_date between '2014-07-01' and '2015-06-30'
and extent.extent_type_id = '278'

group by repository.name
