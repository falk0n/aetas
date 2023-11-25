import re
import os


# just convenience to put all Baustein names into a set
# def baustein_names():
#     file_with_names = "bausteine_names"         # output of extract_bausteine_names.py
#     names = set()
#     with open(file_with_names, "r") as bausteine:
#         for baustein in bausteine:
#             names.add(baustein.strip())
#     return names


def bausteine_names(path_bausteine):
    names = set()
    old_path = os.getcwd()
    os.chdir(path_bausteine)
    for baustein in os.scandir():
        raw_baustein = baustein.name.split(".pdf")[0]
        new_baustein = raw_baustein.replace("CCON", "CON", 1)   # weird file names for CON.X Bausteine from BSIß
        names.add(new_baustein)
    os.chdir(old_path)
    return names


# combine the title lines into one long heading lines:
# - The name of the Baustein titles[0] is not used.
# - Sections titles[2] get the number of the chapter as a prefix, e.g. "1.1 Beschreibung".
# - Subsections (only in chapter 3, describing individual requirements) don't get an enumeration.
# - All parts of the long heading line are separated by "/".
def heading_line(titles):
    heading = titles[1]      # Chapter heading
    if len(titles) > 2:
        chapter_no = titles[1].split(" ")[0]
        heading += "/" + chapter_no + titles[2]
    if len(titles) > 3:
        parts = titles[3].split(" ")
        subsection = " ".join(parts[1:])
        heading += "/" + subsection
    return heading + "\n"


# Read the xml for the given Baustein and return it as a list of its lines.
def read_xml_baustein(baustein):
    xml_file = "xml/" + baustein + ".xml"
    with open(xml_file) as infile:
        content = infile.readlines()
    return content


# parse one Baustein in xml format and create a txt version.
# The xml version is read from subdirectory "xml" (see read_xml_baustein())
# The txt version is written to the subdirectory "txt".
# In the text version:
# - paragraphs are separated by \n\n
# - each paragraph starts with a line of its concatenated chapter/section/subsection names
def parse_baustein(baustein_content):
    result = []

    pattern_title = re.compile("^<title>(.*)</title>$")
    pattern_para = re.compile("^<para>(.*)</para>$")

    titles = []
    numbers = [-1]
    section_open = True

    for line in baustein_content:
        # print(f"Chapter/section: {numbers}")
        if line.startswith("<section"):
            if section_open:
                numbers.append(0)
            section_open = True

        if line.startswith("</section>"):
            if not section_open:
                numbers.pop()
            section_open = False
            titles.pop()

        match_title = pattern_title.match(line)
        if match_title:
            numbers[-1] += 1
            titles.append(str(numbers[-1]) + ". " + match_title.group(1))

        match_para = pattern_para.match(line)
        if match_para:
            absatz = match_para.group(1)
            result.append(heading_line(titles))
            result.append(absatz)
            result.append("\n\n")
    return result


# remove <emphasis ... > and </emphasis> tags from the lines
def clean_emphasis_tags(lines):
    result = []
    # we are looking for these two patterns and want to remove them completely
    pattern_emp_start = re.compile("<emphasis [^>]*>")
    pattern_emp_end = re.compile("</emphasis>")
    for line in lines:
        match_emp_end = pattern_emp_end.search(line)
        if match_emp_end:
            parts = re.split(pattern_emp_end, line)
            line = ''.join(parts)
        match_emp_start = pattern_emp_start.search(line)
        if match_emp_start:
            parts = re.split(pattern_emp_start, line)
            line = ''.join(parts)
        result.append(line)
    return result


# combine all <para> ... </para> inside an itemizedlist with its preceding <para>.
# Assumption: The line before <itemizedlist> is always a paragraph (<para> ... </par>).
def handle_itemizedlist(lines):
    result = []
    pattern_greed_start = re.compile("<itemizedlist>")      # That's how an itemizedlist starts.
    pattern_greed_stop = re.compile("</itemizedlist>")      # That's how it ends.
    pattern_para = re.compile("^<para>(.*)</para>$")        # These are the paragraphs we want to combine.
    greed_state = False
    greed_content = ""
    last_line = lines[0].strip()
    for line in lines[1:]:
        line = line.strip()
        # split the last line for its content
        line_content = ""
        match_para = pattern_para.match(last_line)
        if match_para:
            line_content = match_para.group(1)
        # check if we encounter an itemizedlist and switch to greedy state
        greed_start = pattern_greed_start.search(line)
        if greed_start:
            greed_state = True
            greed_content = ""
            continue

        # greedy state -> concatenate all contents between <para> ... </para>
        if greed_state:
            match_para = pattern_para.match(line)
            if match_para:
                greed_content += " " + match_para.group(1)
            greed_end = pattern_greed_stop.search(line)
            if greed_end:
                greed_state = False
            continue

        # non greedy state -> print last line
        if not greed_state:
            match_para = pattern_para.match(last_line)
            if not match_para:
                result.append(last_line + "\n")
            else:
                new_line = "<para>" + line_content + greed_content + "</para>" + "\n"
                result.append(new_line)
                greed_content = ""
            # save the content of the last line for the next iteration of greediness
            last_line = line.strip()
            continue
    result.append(last_line)

    return result


# write the lines into a textfile for the Baustein
# This is the final part of the text processing pipeline.
def write_txt_file(lines, baustein):
    txt_file = "./txt/" + baustein + ".txt"
    with open(txt_file, "w") as file:
        for line in lines:
            file.write(line)
    file.close()


def main():

    old_path = os.getcwd()
    bsi_path = "/home/falk/work/nlp/corpus/bsi"
    os.chdir(bsi_path)
    bausteine = bausteine_names("./pdf")
    for baustein in bausteine:
        lines_raw = read_xml_baustein(baustein)
        lines_no_lists = handle_itemizedlist(lines_raw)
        lines_parsed = parse_baustein(lines_no_lists)
        lines_clean = clean_emphasis_tags(lines_parsed)
        write_txt_file(lines_clean, baustein)
    os.chdir(old_path)


if __name__ == "__main__":
    main()
