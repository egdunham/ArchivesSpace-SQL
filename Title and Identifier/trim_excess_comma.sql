update archival_object 


set display_string = replace(display_string, ',,', ','), title = (trim(',' from title))



where root_record_id = 1248;