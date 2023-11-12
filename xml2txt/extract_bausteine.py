import re


# just convenience to put all Baustein names into a set
def baustein_names():
    file_with_names = "bausteine_names"         # output of extract_bausteine_names.py
    names = set()
    with open(file_with_names, "r") as bausteine:
        for baustein in bausteine:
            names.add(baustein.strip())
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
    return start_lines


# extract all lines belonging to baustein into a file named baustein.xml
# start and final <section> </section> tags are omitted.
# The <informaltable> </informaltable> section is omitted.
def extract_baustein(baustein, start_line, content):
    filename = "xml/" + baustein + ".xml"
    section_level = 1
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
    bausteine = baustein_names()                    # every Baustein
    # bausteine = ["SYS.1.1 Allgemeiner Server"]    # Baustein for testing

    kompendium = "bsi_grundschutz_2023.xml"         # XML of IT-Grundschutzkompendium as provided by BSI
    with open(kompendium) as kompendium:
        content = kompendium.readlines()

    start_lines = baustein_start_lines(bausteine, content)
    for baustein, line_no in start_lines.items():
        extract_baustein(baustein, line_no, content)


if __name__ == "__main__":
    main()
