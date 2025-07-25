import os
import csv
import filetype

#result = os.path.ismount('\\libfile.lib.asu.edu\share')

# Add filepaths for the root folder and error CSV
filepath = r"C:\Users\egdunham\Desktop\Check"

for (root, dirs, files) in os.walk(filepath, topdown=True):
    for file in files:
        filepath = os.path.join(root, file)
        kind = filetype.guess(filepath)

        if kind is None:
            row = [filepath]
            os.remove(filepath)
