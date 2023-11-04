from enum import Enum
import re

from modules import fscutils as fsc


#
# At the end of ingest03.py we know everything to load an IT-Grundschutz Baustein.
# The BSILoader class ties everything together and provides a simple interface.
# It is modelled after langchain.document_loaders.
#
class Linetype(Enum):
    CONTENT = 0
    CHAPTER = 1
    SECTION = 2
    REQUIREMENT = 3
    HEADER = 4
    FOOTER = 5


# classify the type of line (content, header, footer, chapter heading, ... )
# This function is highly specific for IT-Grundschutz Document.
def classify_line(line, name_baustein, id_baustein):
    result = Linetype.CONTENT
    if re.match(r"\d+\.\d+\. ", line["page_content"]) is not None:
        result = Linetype.SECTION
    elif re.match(r"\d+\. ", line["page_content"]) is not None:
        result = Linetype.CHAPTER
    elif re.match(r"Seite \d+ von \d+", line["page_content"]) is not None:
        result = Linetype.FOOTER
    elif re.match(name_baustein, line["page_content"]) is not None:
        result = Linetype.HEADER
    elif re.match(id_baustein + r"\.A\d+ ", line["page_content"]) is not None:
        result = Linetype.REQUIREMENT
    return result


# annotate each line with chapter, section and  (if applicable) the name of the requirement
# keep only content lines (no document title, header, footers; chapter, section and requirement names
def annotate_lines(lines, baustein, id_baustein):
    chapter = False
    chapter_name = ""
    section = False
    section_name = ""
    requirement = False
    requirement_name = ""
    docs_lines_annotated = []
    for line in lines:
        linetype = classify_line(line, baustein, id_baustein)
        if linetype == Linetype.CHAPTER:
            chapter_name = line["page_content"]
            chapter = True
            section = False
            section_name = ""
            requirement = False
            requirement_name = ""
        elif linetype == Linetype.SECTION:
            section_name = line["page_content"].replace("\n", "")           # no line breaks. It's ugly and I know it.
            section = True
            requirement = False
            requirement_name = ""
        elif linetype == Linetype.REQUIREMENT:
            requirement_name = line["page_content"].replace("\n", "")       # no line breaks. It's ugly and I know it.
            requirement = True
        # annotate CONTENT lines with chapter, section and requirement
        if linetype == Linetype.CONTENT:
            line["metadata"]["baustein_name"] = baustein
            line["metadata"]["baustein_id"] = id_baustein
            line["metadata"]["chapter"] = chapter
            line["metadata"]["section"] = section
            line["metadata"]["requirement"] = requirement
            if section:
                line["metadata"]["section_name"] = section_name
            if requirement:
                line["metadata"]["requirement_name"] = requirement_name
            if chapter:
                line["metadata"]["chapter_name"] = chapter_name
                docs_lines_annotated.append(line)
    return docs_lines_annotated


#
# Parse the line by line representation of the IT-Grundschutz Baustein:
# -> return a list of Document (to keep in langchain world)
# -> each Document is one section (or requirement) with appropriate annotations in the metadata
#
def parse(docs_raw):
    docs_lines = fsc.conv_document_list_to_dicts(docs_raw)  # convert list of Document into dict()
    foo = docs_lines[0]["metadata"]["source"]               # source is the only guaranteed metadata field
    bar = foo.split("/")[-1]                                # do some string gymnastics to get the name of the Baustein
    baustein_name = bar[0:-14]                              # we don't want the extensions
    baustein_id = baustein_name.split(" ")[0]               # extract ID of Baustein from metadata

    # annotate lines, keep only content lines -> This is the heavy lifting.
    docs_annotated = annotate_lines(docs_lines, baustein_name, baustein_id)

    # merge chunks with the same chapter, section and requirements (=sub section)
    docs_combined = []
    current = docs_annotated[0]
    for next_chunk in docs_annotated[1:]:
        if (current["metadata"].get("chapter_name", 0) == next_chunk["metadata"].get("chapter_name", 0)) and \
                (current["metadata"].get("section_name", 0) == next_chunk["metadata"].get("section_name", 0)) and \
                (current["metadata"].get("requirement_name", 0) == next_chunk["metadata"].get("requirement_name", 0)):
            current["page_content"] += " " + next_chunk["page_content"]
        else:
            # remove all remaining \n from page_content (the last remnant from PDFMiner)
            new_content = current["page_content"].replace("\n", "")
            current["page_content"] = new_content
            docs_combined.append(current)
            current = next_chunk
    docs_combined.append(current)

    # convert list of dict() back to list of Document and return the result
    docs_final = fsc.conv_dict_list_to_documents(docs_combined)
    return docs_final
