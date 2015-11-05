/* Returns the number of special format items excluding photographs */
select sum(extent.number), enumeration_value.value

from archivesspace.accession
join archivesspace.extent on accession.id = extent.accession_id
right join archivesspace.enumeration_value on extent.extent_type_id = enumeration_value.id

where extent_type_id != 278
and extent_type_id != 1288
and extent_type_id != 1370
and enumeration_value.value != 'photographic_prints'
and enumeration_value.value != 'photographic_slides'
and enumeration_value.value != 'Glass Plate Negatives'
and enumeration_value.value != 'Photographs'
and enumeration_value.value != 'Images'

group by extent_type_id
