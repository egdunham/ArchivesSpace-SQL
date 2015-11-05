/* Integers entered in user defined Integer 1 need to be added separately until migraion is complete */
select sum(extent.number)

from archivesspace.accession
join archivesspace.extent on accession.id = extent.accession_id
join archivesspace.enumeration_value on extent.extent_type_id = enumeration_value.id

where
(enumeration_value.value = 'photographic_prints')
or (enumeration_value.value = 'photographic_slides')
or (enumeration_value.value = 'Glass Plate Negative(s)')
or (enumeration_value.value = 'Photograph(s)')
or (enumeration_value.value = 'Image(s)')
