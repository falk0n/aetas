import os
import json

#
# bsi_json.py
# Combine all Baustein.txt files into one big txt file.
# Each line has the format ID|Baustein|chapter|section|requirement|content
# where ID is the ID of the Baustein (e.g. SYS.1.1),
# BAUSTEIN is the name of the Baustein (e.g. Allgemeiner Server), etc.
#
# The main idea of this transformation is to move all BSI specific preprocessing out of AETAS.
# The second idea is to have exactly one line per document which can be easily parsed.
# It has been verified that "|" does not occur in the baustein.txt files. Splitting by "|" is thus unique.
#


def process(filename):
    baustein_id, baustein_name = filename.replace(".txt", "").split(" ", maxsplit=1)
    result = []
    with open(filename, "r", encoding="utf-8-sig") as file:
        while True:
            metadata = file.readline().strip()
            if len(metadata) == 0:
                break
            # handle all the metadata attributes
            out_line_parts = [baustein_id, baustein_name]
            out_line_parts.extend(metadata.split("/", maxsplit=2))
            if len(out_line_parts) < 4:
                out_line_parts.append("kein Abschnitt")
            if len(out_line_parts) < 5:
                out_line_parts.append("keine Anforderung")
            out_line_parts.append(file.readline().strip())
            out_line = out_line_parts[0]
            for i in range(1, len(out_line_parts)):
                out_line += "|" + out_line_parts[i]
            out_line += "\n"
            result.append(out_line)
            file.readline()
    return result


def main():
    filedir = "/home/falk/work/nlp/corpus/bsi/txt"
    out_file_name = "/home/falk/work/nlp/corpus/bsi/bsi_all.txt"
    old_path = os.getcwd()
    os.chdir(filedir)
    with open(out_file_name, "w") as out_file:
        for filename in os.listdir(filedir):
            for line in process(filename):
                out_file.write(line)
    os.chdir(old_path)


if __name__ == "__main__":
    main()
