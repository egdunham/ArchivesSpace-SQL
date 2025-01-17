import os
import csv
import filetype

#result = os.path.ismount('\\libfile.lib.asu.edu\share')

# Add filepaths for the root folder and error CSV
filepath = r"\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\2014_04818\Drive 2\New Photos"

for (root,dirs,files) in os.walk(filepath, topdown=True):
    for file in files:
            filepath = os.path.join(root, file)
            kind = filetype.guess(filepath)


            if kind is None:
                    row = [filepath]
                    os.remove(filepath)