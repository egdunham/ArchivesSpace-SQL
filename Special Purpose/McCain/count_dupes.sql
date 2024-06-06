select distinct * from (select master_md5_checksums, count(*) c from master_md5_set 
where original_media_id not in ("ms_cm_mss_114","ms_cm_mss_409_186")
and master_md5_checksums not in ("d41d8cd98f00b204e9800998ecf8427e","194577a7e20bdcc7afbb718f502c134c")
group by master_md5_checksums)  as okfine where c > 1