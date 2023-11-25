import re
import os


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


# find the starting line of each Baustein in the big Kompendium
def baustein_start_lines(names, content):
    start_lines = dict()
    for line_no in range(len(content)):
        pattern = re.compile("^<title>(.*)</title>$")
        match = pattern.search(content[line_no])
        if match:
            baustein_name = match.group(1)
            if baustein_name in names:
                start_lines[baustein_name] = line_no
                print(f"found Baustein {baustein_name}")
    return start_lines


# extract all lines belonging to baustein into a file named baustein.xml
# start and final <section> </section> tags are omitted.
# The <informaltable> </informaltable> section is omitted.
def extract_baustein(baustein, start_line, content):
    filename = "./xml/" + baustein + ".xml"
    section_level = 1
    print(f"Start with: {filename}")
    with open(filename, "w") as file:
        print_flag = True
        for line_no in range(start_line, len(content)):
            line = content[line_no]
            if line.startswith("<section"):
                section_level += 1
            if line.startswith("</section>"):
                section_level -= 1
            if section_level == 0:
                break
            if line.startswith("<informaltable"):
                print_flag = False
            if print_flag:
                file.write(line)
            if line.startswith("</informaltable"):
                print_flag = True
    file.close()


def main():
    # bsi_path should have subdirectories pdf, xml and txt for Bausteine in different formats.
    # bsi_path/pdf should contain the pdf versions of the Bausteine as downloaded from BSI website.
    bsi_path = "/home/falk/work/nlp/corpus/bsi"
    old_path = os.getcwd()
    os.chdir(bsi_path)
    bausteine = bausteine_names("./pdf")
    print(f"Bausteine: {bausteine}")
    # bausteine = ["SYS.1.1 Allgemeiner Server"]

    kompendium = "./kompendium/bsi_grundschutz_2023.xml"         # XML of IT-Grundschutzkompendium as provided by BSI
    with open(kompendium) as kompendium:
        content = kompendium.readlines()

    start_lines = baustein_start_lines(bausteine, content)
    print(f"Anzahl start_lines: {start_lines}")
    for baustein, line_no in start_lines.items():
        extract_baustein(baustein, line_no, content)

    os.chdir(old_path)


if __name__ == "__main__":
    main()
