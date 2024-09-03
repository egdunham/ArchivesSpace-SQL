import os
import csv
import filetype

#result = os.path.ismount('\\libfile.lib.asu.edu\share')

# Add filepaths for the root folder and error CSV
filepath = r"C:\Users\egdun\OneDrive\Desktop\test_data"
csv_output = os.path.normpath(r"C:\Users\egdun\OneDrive\Desktop\errors.csv")

with open(csv_output, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["filepath"])

    for (root,dirs,files) in os.walk(filepath, topdown=True):
        for file in files:
                filepath = os.path.join(root, file)
                kind = filetype.guess(filepath)


                if kind is None:
                        row = [filepath]
                        csvwriter.writerow(row)
                        os.remove(filepath)