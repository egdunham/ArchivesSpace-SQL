
/* THE "PROCESSED DURING" PART DOES NOT WORK */

select resource.identifier, resource.title, event.event_type_id, enumeration_value.value

from archivesspace.event_link_rlshp

join event on event.id = event_link_rlshp.event_id

join enumeration_value on event.event_type_id = enumeration_value.id

join enumeration on enumeration_value.enumeration_id = enumeration.id

join resource on event_link_rlshp.resource_id = resource.id

where enumeration_value.value = 'processed'
