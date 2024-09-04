select 
(select count(*) from master_md5_set where Discard like "Appraise%" and original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")) as appraise,
(select count(*) from master_md5_set where Discard like "TRUE%" and original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")) as discard,
(select count(*) from master_md5_set where Discard like "Processed%" and original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")) as processed,
(select count(*) from master_md5_set where (Discard like "0" or Discard is null)and original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")) as toDo,
(select count(*) from master_md5_set where (Discard="Unevaluated Dupe")and original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")) as unevalDupe