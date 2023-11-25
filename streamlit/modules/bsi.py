from enum import Enum
import re

from modules import fscutils as fsc


#
# Functions for parsing the text in the PDF documents for BSI IT-Grundschutz.
# Main entry point is parse().
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
    # Next one is the prefix of subsection specifying exactly one requirement.
    # Because we decided to split either chapters are sections it is now treated like content.
    # elif re.match(id_baustein + r"\.A\d+ ", line["page_content"]) is not None:
    #    result = Linetype.REQUIREMENT
    return result


# annotate each line with chapter, section and  (if applicable) the name of the requirement
# keep only content lines (no document title, header, footers; chapter, section and requirement names
def annotate_lines(lines, baustein, id_baustein):
    chapter = False
    chapter_name = "none"
    section = False
    section_name = "none"
    # requirement = False
    # requirement_name = ""
    docs_lines_annotated = []
    for line in lines:
        linetype = classify_line(line, baustein, id_baustein)
        if linetype == Linetype.CHAPTER:
            chapter_name = line["page_content"]
            chapter = True
            section = False
            section_name = "none"
            # requirement = False
            # requirement_name = ""
        elif linetype == Linetype.SECTION:
            section_name = line["page_content"].replace("\n", "")           # no line breaks. It's ugly and I know it.
            section = True
            # requirement = False
            # requirement_name = ""
        # LineType.REQUIREMENT is not used any longer
        # elif linetype == Linetype.REQUIREMENT:
        #    requirement_name = line["page_content"].replace("\n", "")       # no line breaks. It's ugly and I know it.
        #    requirement = True
        # annotate lines with chapter, section and requirement
        if linetype in [Linetype.CONTENT, Linetype.CHAPTER, Linetype.SECTION]:
            line["metadata"]["baustein_name"] = baustein
            line["metadata"]["baustein_id"] = id_baustein
            line["metadata"]["chapter_name"] = "none"
            line["metadata"]["section_name"] = "none"
            # line["metadata"]["requirement"] = requirement
            if section:
                line["metadata"]["section_name"] = section_name
            # if requirement:
            #    line["metadata"]["requirement_name"] = requirement_name
            if chapter:
                line["metadata"]["chapter_name"] = chapter_name
                docs_lines_annotated.append(line)
    return docs_lines_annotated


#
# Return true if the current chapter continues (aggregate_into_chapters == True)
# Return true if the current section continues (aggregate_into_chapters == False)
# This functions serves as shorthand for parse to make it easier readable.
#
def chunk_continues(current, next_chunk, aggregate_into_chapters):
    # True if current and next_chunk are part of the same CHAPTER
    result = current["metadata"].get("chapter_name", 0) == next_chunk["metadata"].get("chapter_name", 0)
    if not aggregate_into_chapters:
        # True if current and next chunk are part of the same SECTION
        result = result and current["metadata"].get("section_name", 0) == next_chunk["metadata"].get("section_name", 0)
    return result


# add an annotation that is used whenever this chunk should be cited.
# The form of the citation is Baustein ID / Section Name
# If the chunk is not part of a section it is Baustein ID / chapter name.
# Every chunk is/should be part of a chapter.
def add_citation(chunk):
    metadata = chunk["metadata"]
    zitat = metadata["baustein_id"] + " / " + metadata["section_name"]
    if metadata["section_name"] == "none":
        zitat = metadata["baustein_id"] + " / " + metadata["chapter_name"]
    metadata["citation"] = zitat.strip()
    return


#
# Parse the line by line representation of the IT-Grundschutz Baustein:
# -> return a list of Document (to keep in langchain world)
# -> each Document is one section or chapter depending on the value of aggregate_into_chapters
# -> Annotations added to each Document: baustein_name, baustein_id, chapter_name, section_name
#
def parse(docs_raw, aggregate_into_chapters):
    docs_lines = fsc.conv_document_list_to_dicts(docs_raw)  # convert list of Document into dict()
    foo = docs_lines[0]["metadata"]["source"]               # source is the only guaranteed metadata field
    bar = foo.split("/")[-1]                                # filename (last part of path) includes Baustein info
    baustein_name = bar[0:-14]                              # Baustein name = filename without extensions
    baustein_id = baustein_name.split(" ")[0]               # extract ID of Baustein

    # annotate lines, keep only content lines -> This is the heavy lifting.
    docs_annotated = annotate_lines(docs_lines, baustein_name, baustein_id)

    # merge chunks with the same chapter and section
    docs_combined = []
    current = docs_annotated[0]
    for next_chunk in docs_annotated[1:]:
        if chunk_continues(current, next_chunk, aggregate_into_chapters):
            current["page_content"] += " " + next_chunk["page_content"]
        else:
            # remove all remaining \n from page_content (the last remnant from PDFMiner)
            # Check if this is still necessary
            new_content = current["page_content"].replace("\n", "")
            current["page_content"] = new_content
            add_citation(current)
            docs_combined.append(current)
            current = next_chunk
    docs_combined.append(current)

    # convert list of dict() back to list of Document and return the result
    docs_final = fsc.conv_dict_list_to_documents(docs_combined)
    return docs_final
