#splitting hotspots based on shared or population specific for contig analysis
#will pull hotspot position from *hot_vs_contigbound.txt file and return a file that has either shared or pop-specific per line
#to run script: python3 SplitHot.py <hot vs contig comparison file> <shared hotspots file> <output file>
#Author: Alice Shanfelter, May 2018

'''to get sum for each catergory
grep -i "Shared" <file> | awk '{sum+=$2} END {print sum}'
will need to alter "Shared" or "Pop-Specific" and column number (2-7)
'''
import sys

#pulls hotspot positions from contig comparison file
#returns hotspot starting positions in a list
def pull_hotspot_pos():
    cb_hot_file = sys.argv[1]
    hot_start = []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith("Hotspot"):
                new_line = line.split()
                split_value = new_line[1].split("-")
                hot_start.append(split_value[0])
    return hot_start

#pulling each hotspot category with following functions
def within():
    cb_hot_file = sys.argv[1]
    within_values = []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within hotspot"):
                new_line = line.split(":")
                within_values.append(int(new_line[1].strip("\n")))
    return within_values

def within_1kb():
    cb_hot_file = sys.argv[1]
    within_values_1kb= []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within 1kb"):
                new_line = line.split(":")
                within_values_1kb.append(int(new_line[1].strip("\n")))
    return within_values_1kb

def within_2kb():
    cb_hot_file = sys.argv[1]
    within_values_2kb= []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within 2kb"):
                new_line = line.split(":")
                within_values_2kb.append(int(new_line[1].strip("\n")))
    return within_values_2kb

def within_5kb():
    cb_hot_file = sys.argv[1]
    within_values_5kb= []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within 5kb"):
                new_line = line.split(":")
                within_values_5kb.append(int(new_line[1].strip("\n")))
    return within_values_5kb

def within_10kb():
    cb_hot_file = sys.argv[1]
    within_values_10kb= []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within 10kb"):
                new_line = line.split(":")
                within_values_10kb.append(int(new_line[1].strip("\n")))
    return within_values_10kb

def within_20kb():
    cb_hot_file = sys.argv[1]
    within_values_20kb= []
    with open(cb_hot_file, 'r') as contig_file:
        for line in contig_file:
            if line.startswith(" Contig Boundaries within 20kb"):
                new_line = line.split(":")
                within_values_20kb.append(int(new_line[1].strip("\n")))
    return within_values_20kb

#pulls shared hotspot positions and returns them as a list
def pull_shared_hot():
    shared_file = sys.argv[2]
    shared_hot = []
    with open(shared_file, 'r') as shared:
        for line in shared:
            if line.startswith("Hotspot"):
                new_line = line.split()
                shared_hot.append(new_line[2])
    return shared_hot

#compare shared and hotspot contig file to separate shared and pop specific
#returns a list with either shared or pop-specific for each hotspot
def compare():
    contig_hot = pull_hotspot_pos()
    shared_hot = pull_shared_hot()
    hot_type = []
    for value in contig_hot:
        if value in shared_hot:
            hot_type.append("Shared")
        else:
            hot_type.append("Pop-Specific")
    return hot_type

#Getting counts of hotspots within contig boundaries for shared and population specific hotspots
def write():
    hot_type = compare()
    within_hot = within()
    within_hot = ["0" if y == 0 else "1" for y in within_hot]
    within_1kb_hot = within_1kb()
    within_1kb_hot = ["0" if y == 0 else "1" for y in within_1kb_hot]
    within_2kb_hot = within_2kb()
    within_2kb_hot = ["0" if y == 0 else "1" for y in within_2kb_hot]
    within_5kb_hot = within_5kb()
    within_5kb_hot = ["0" if y == 0 else "1" for y in within_5kb_hot]
    within_10kb_hot = within_10kb()
    within_10kb_hot = ["0" if y == 0 else "1" for y in within_10kb_hot]
    within_20kb_hot = within_20kb()
    within_20kb_hot = ["0" if y == 0 else "1" for y in within_20kb_hot]
    output = sys.argv[3]
    with open(output, 'a') as out:
        header = "Hot Type\tWithinHot\tWithin1kbHot\tWithin2kbHot\tWithin5kbHot\tWithin10kbHot\tWithin20kbHot\n"
        out.write(header)
        for index, value in enumerate(hot_type):
            final = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (value, within_hot[index],within_1kb_hot[index],within_2kb_hot[index],within_5kb_hot[index],within_10kb_hot[index],within_20kb_hot[index])
            out.write(final)

write()
