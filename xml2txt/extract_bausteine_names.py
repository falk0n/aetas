import os


# filename should be a list of pdf files of IT-Grundschutz Bausteine
# filename = "bausteine_files"
#
# # print to stdout a list of the Bausteine
# with open(filename, "r") as file:
#     for line in file.readlines():
#         baustein = line.split(".pdf")[0]
#         print(baustein)


def extract_bausteine_names(path_bausteine):
    names = set()
    old_path = os.getcwd()
    os.chdir(path_bausteine)
    for baustein in os.scandir():
        new_baustein = baustein.name.split(".pdf")[0]
        names.add(new_baustein)
    os.chdir(old_path)
    return names
