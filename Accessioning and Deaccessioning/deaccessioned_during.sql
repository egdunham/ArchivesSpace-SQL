select distinct deaccession.accession_id

from deaccession

left join date on deaccession.id = date.deaccession_id

left join extent on deaccession.id = extent.deaccession_id

left join enumeration_value on deaccession.scope_id = enumeration_value.id

where enumeration_value.value = "whole"