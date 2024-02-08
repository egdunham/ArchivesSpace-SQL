import requests
import os
import csv

# Get list of MARC records to download
merge_input = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\loc_matches.csv")

# Set path to output file
csv_output = os.path.normpath(r"C:\Users\egdunham\Dropbox (ASU)\__MyFiles\Desktop\filter_results.csv")

with open(merge_input,'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    with open(csv_output,'w', newline='', encoding="utf-8") as csvout:
        writer = csv.writer(csvout)
        headerRow = {"Search Name", "LOC Name", "LOC URI", "Is Director"}
        writer.writerow(headerRow)

        for row in reader:
            director = "False"
            record = requests.get(row[3] + ".json").json()
            #pprint(record)
            for id in record:
                type = id.get("@type")

                for item in type:
                    if item == "http://www.loc.gov/mads/rdf/v1#Source" and id.get("http://www.loc.gov/mads/rdf/v1#citationNote") != None:

                        note = id.get("http://www.loc.gov/mads/rdf/v1#citationNote")

                        for entry in note:
                            value = entry.get("@value")

                            if "director" in value or "directed" in value:
                                director = True

            row = [row[1], row[2], row[3], director]
            writer.writerow(row)
