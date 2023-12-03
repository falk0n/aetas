import os
import json

#
# bsi_json.py
# Combine all Baustein.txt files into one big json file.
# Format is [ {"page_content": <content>, ",metadata": <metadata_dict>}, ... ]
# where metadata_dict is a dictionary with the metadata attributes.
# Possible values are: source, baustein_id, baustein_name, chapter, section, subsection.
#
# The main idea of this transformation is to move all BSI specific preprocessing out of AETAS.
# The json format is intended to be used by Langchain JSONLoader which handles attribute names generically.
#


def process(filename):
    meta_names = ["chapter", "section", "subsection"]
    baustein_id, baustein_name = filename.replace(".txt", "").split(" ", maxsplit=1)
    result = []
    with open(filename, "r", encoding="utf-8-sig") as file:
        while True:
            metadata = file.readline().strip()
            if len(metadata) == 0:
                break
            # handle all the metadata attributes
            source = baustein_id + "/" + baustein_name + "/" + metadata
            metadata_dict = dict({"baustein_id": baustein_id,
                                  "baustein_name": baustein_name,
                                  "source": source})
            meta_values = metadata.split("/", maxsplit=2)
            for i in range(len(meta_values)):
                metadata_dict[meta_names[i]] = meta_values[i]
            # handle page_content and put everything together
            content = file.readline().strip()
            entry = dict({"page_content": content})
            entry["metadata"] = metadata_dict
            result.append(entry)
            file.readline()
    return result


def main():
    filedir = "/home/falk/work/nlp/corpus/bsi/txt"
    out_file_name = "/home/falk/work/nlp/corpus/bsi/bsi_all.json"
    results = []
    old_path = os.getcwd()
    os.chdir(filedir)
    for filename in os.listdir(filedir):
        lines = process(filename)
        results.extend(lines)
    os.chdir(old_path)
    with open(out_file_name, "w") as out_file:
        out_file.write(json.dumps(results))


if __name__ == "__main__":
    main()
