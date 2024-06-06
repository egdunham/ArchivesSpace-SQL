@ECHO OFF
SET COUNT=1
SET DESTINATION="\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\Final_Heirarchy\Presidential_Campaign_2008\Photographs\103_2008_October_11\"
:MyLoop
    IF "%COUNT%" == "6" GOTO EndLoop
    mkdir %DESTINATION%%COUNT%
    SET /A COUNT+=1
    GOTO MyLoop
:EndLoop