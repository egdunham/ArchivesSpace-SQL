from docx2pdf import convert
import win32com.client as win32

import csv

input = r"C:\Users\egdunham\Desktop\input.csv"

with open(input, 'r', encoding='windows-1252') as csvin:
    reader = csv.reader(csvin)
    next(reader, None)

    for row in reader:
        # Isolate file name and extension
        path_split = row[0].rsplit("\\", 1)
        file_extension = row[0].rsplit(".", 1)[1]

        # PARSE OUT TO VARIOUS FUNCTIONS FROM HERE
        # FOR DOC FIRST SEND TO DOCX THEN PDF
        # If doc or docx format, add "_migrated" and migrate to .pdf
        if file_extension == "docx":

            new_name = str(path_split[0]) + "\\" + str(path_split[1].rsplit(".", 1)[0]) + "_migrated.pdf"
            convert(row[0], new_name)
