select subject.title, archival_object.repo_id, resource.repo_id, repository.name

from archivesspace.subject
	join subject_rlshp on subject_rlshp.subject_id = subject.id

	left join resource on resource.id = subject_rlshp.resource_id

	left join archival_object on subject_rlshp.archival_object_id = archival_object.id

	left join repository on archival_object.repo_id = repository.id

where subject.title like '%TERM%'
