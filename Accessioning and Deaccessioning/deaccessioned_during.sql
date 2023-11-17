select distinct *

from deaccession

left join date on deaccession.id = date.deaccession_id

-- left join extent on deaccession.id = extent.deaccession_id

left join enumeration_value on deaccession.scope_id = enumeration_value.id       

where enumeration_value.value = "whole"
-- and extent.extent_type_id = 278