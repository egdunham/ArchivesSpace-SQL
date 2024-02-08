select distinct * 

from accession

left join user_defined on accession.id = user_defined.accession_id

left join extent on extent.accession_id = accession.id

where (user_defined.text_2 like "%182%" or user_defined.text_4 like "%182%");