
# filename should be a list of pdf files of IT-Grundschutz Bausteine
filename = "bausteine_files"

# print to stdout a list of the Bausteine
with open(filename, "r") as file:
    for line in file.readlines():
        baustein = line.split(".pdf")[0]
        print(baustein)
