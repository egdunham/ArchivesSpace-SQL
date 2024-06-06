@ECHO OFF

set from_directory="\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\Preservation Files\ms_cm_mss_409_939\Photos\040108_mccainPhotos\"
set to_directory="\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\Final_Heirarchy\Presidential_Campaign_2008\Photographs\1_2008_April_1\1\"

move %from_directory%*.JPG %to_directory%