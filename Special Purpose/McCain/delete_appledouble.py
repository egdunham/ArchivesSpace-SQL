import os
import csv
import filetype

# Add filepaths for the root folder and error CSV
filepath = r"\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\2014_04818\Drive 2\Render Files"

# Read through specified directory and remove all subdirectories called ".AppleDouble"
for (root, dirs, files) in os.walk(filepath, topdown=True):
    for file in files:
        filepath = os.path.join(root, file)

        if "AppleDouble" in filepath:
            os.remove(filepath)
            print(".AppleDouble removed")

