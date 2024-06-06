update master_md5_set as t1,
(select id from master_md5_set where original_media_id = "ms_cm_mss_409_939" and filepath like "%/033108_mccainPhotos%DS_STORE" and (Discard not like "TRUE: Dupe" or Discard is null)) as t2
set t1.Discard = "TRUE"
where t1.id in (t2.id)