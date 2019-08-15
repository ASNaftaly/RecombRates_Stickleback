#comparing hotspot location to contig boundaries
#got contig boundaries from bam file using following command:
#cut -d '     ' -f 1,2 <mpileup file from samtools> | awk 'BEGIN {chr="";start=-1;end=-1} {if(chr!=$1 || int($2)!=end+1) { if(chr!="") {printf("%s:%d-%d\n",chr,start,end);} chr=$1;start=int($2);end=int($2);} else {end=end+1;}} END {if(chr!="") {printf("%s:%d-%d\n",chr,start,end); } }' >> <output file>
#Want to see if hotspots tend to fall in contig boundaries; if so, this could mean that hotspots are caused by these boundaries versus being real hotspots
#to do this, will see how many hotspots fall within 1, 2, 5, 10, 20 kb of contig boundaries (will adjust this as results come in)
#to run script: python3 CompareContigBoundvsHot.py <contig boundaries file> <hotspot positions file> <output file>
#Author: Alice Shanfelter, May 2018

import sys
import time

#pulling contig boundaries from contig_boundaries file
#file in format:
#chrX:start-stop for each contig
#returns list with format: [start contig 1, end contig 1, start contig 2, end contig 2, ..., start contig n, end contig n]
def pull_contigs():
    contig_file = sys.argv[1]
    contig_list = []
    with open(contig_file, 'r') as contig:
        for line in contig:
            line = line.strip("\n")
            new_line = line.split(":")
            contig_list += new_line[1].split("-")
    return contig_list

#pulls hotspots from hotspot position files
#format: hot start  hot end for each line
#returns list in format: [hot 1 start, hot 1 end, hot 2 start, hot 2 end, ..., hot n start, hot n end]
def pull_hot():
    hotspot_file = sys.argv[2]
    hot_list = []
    with open(hotspot_file, 'r') as hot:
        for line in hot:
            hot_list += line.split()
    return hot_list

#Comparing contig boundaries with hotspots
#need to see if hotspot midpoint is within xkb of contig boundary (contig end y to contig start y + 1)
#produces the number of boundaries within hotspots, not number of hotspots within boundaries
'''def compare():
    contig_list = pull_contigs()
    contig_start = contig_list[0::2]
    contig_end = contig_list[1::2]
    mid_hot = pull_hot()
    output = "PS1_hot_vs_contigbound.txt" #sys.argv[3]
    with open(output, 'a') as out:
        x = 1
        y = 0
        within_cb = 0
        within_1kb_cb = 0
        within_2kb_cb = 0
        within_5kb_cb = 0
        within_10kb_cb = 0
        within_20kb_cb = 0
        while y < len(contig_end)-1:
            for value in mid_hot:
                #if hotspot midpoint is in the contig boundary
                if int(contig_end[y]) <= int(value) <= int(contig_start[x]):
                    within_cb += 1
                    towrite = "Within Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
                elif (int(contig_end[y])-1000) <= int(value) <= (int(contig_start[x])+1000):
                    within_1kb_cb += 1
                    towrite = "Within 1kb of Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
                elif (int(contig_end[y])-2000) <= int(value) <= (int(contig_start[x])+2000):
                    within_2kb_cb += 1
                    towrite = "Within 2kb of Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
                elif (int(contig_end[y])-5000) <= int(value) <= (int(contig_start[x])+5000):
                    within_5kb_cb += 1
                    towrite = "Within 5kb of Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
                elif (int(contig_end[y])-10000) <= int(value) <= (int(contig_start[x])+10000):
                    within_10kb_cb += 1
                    towrite = "Within 10kb of Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
                elif (int(contig_end[y])-20000) <= int(value) <= (int(contig_start[x])+20000):
                    within_20kb_cb += 1
                    towrite = "Within 20kb of Boundary:\n Contig Boundary Start: %s\n Contig Boundary End: %s\n Hotspot Midpoint: %s\n\n" % (contig_end[y],contig_start[x],value)
                    out.write(towrite)
            x += 1
            y += 1
        #Summary lines
        onekb = within_cb + within_1kb_cb
        twokb = within_cb + within_1kb_cb + within_2kb_cb
        fivekb = within_cb + within_1kb_cb + within_2kb_cb + within_5kb_cb
        tenkb = within_cb + within_1kb_cb + within_2kb_cb + within_5kb_cb + within_10kb_cb
        twentykb = within_cb + within_1kb_cb + within_2kb_cb + within_5kb_cb + within_10kb_cb + within_20kb_cb
        summary = "\n\n\n\nSummary:\n\n Total hotspots within boundaries: %s\n Total hotspots within 1kb of boundaries: %s\n Total hotspots within 2kb of boundaries: %s\n Total hotspots within 5kb of boundaries: %s\n Total hotspots within 10kb of boundaries: %s\n Total hotspots within 20kb of boundaries: %s\n" % (within_cb, onekb, twokb, fivekb, tenkb, twentykb)
        out.write(summary)'''

#Comparing contig boundaries with hotspots
#need to see if hotspot midpoint is within xkb of contig boundary (contig end y to contig start y + 1)
def compare():
    contig_list = pull_contigs()
    contig_list = [int(i) for i in contig_list]
    contig_start = contig_list[0::2]
    del contig_start[0]
    contig_end = contig_list[1::2]
    del contig_end[-1]
    hot_list = pull_hot()
    hot_list = [int(i) for i in hot_list]
    hot_start = hot_list[0::2]
    hot_end = hot_list[1::2]
    output = sys.argv[3]
    with open(output, 'a') as out:
        z = 0
        within_hotspot = 0
        within_1kb_hot = 0
        within_2kb_hot = 0
        within_5kb_hot = 0
        within_10kb_hot = 0
        within_20kb_hot = 0
        total_within_hot = 0
        total_within_1kb_hot = 0
        total_within_2kb_hot = 0
        total_within_5kb_hot = 0
        total_within_10kb_hot = 0
        total_within_20kb_hot = 0
        while z < len(hot_start):
            for index, value in enumerate(contig_end):
                #if contig boundary falls completely within hotspot
                if hot_start[z] <= value and hot_end[z] >= contig_start[index]:
                    within_hotspot += 1
                elif hot_start[z]-1000 <= value and hot_end[z]+1000 >= contig_start[index]:
                    within_1kb_hot += 1
                elif hot_start[z]-2000 <= value and hot_end[z]+2000 >= contig_start[index]:
                    within_2kb_hot += 1
                elif hot_start[z]-5000 <= value and hot_end[z]+5000 >= contig_start[index]:
                    within_5kb_hot += 1
                elif hot_start[z]-10000 <= value and hot_end[z]+10000 >= contig_start[index]:
                    within_10kb_hot += 1
                elif hot_start[z]-20000 <= value and hot_end[z]+20000 >= contig_start[index]:
                    within_20kb_hot += 1
            each_hot = "Hotspot: %s-%s\n Contig Boundaries within hotspot: %s\n Contig Boundaries within 1kb of hotspot: %s\n Contig Boundaries within 2kb of hotspot: %s\n Contig Boundaries within 5kb of hotspot: %s\n Contig Boundaries within 10kb of hotspot: %s\n Contig Boundaries within 20kb of hotspot: %s\n\n" % (hot_start[z],hot_end[z],within_hotspot, within_1kb_hot, within_2kb_hot, within_5kb_hot, within_10kb_hot, within_20kb_hot)
            out.write(each_hot)
            if within_hotspot >= 1:
                total_within_hot += 1
            if within_1kb_hot >= 1:
                total_within_1kb_hot += 1
            if within_2kb_hot >= 1:
                total_within_2kb_hot += 1
            if within_5kb_hot >= 1:
                total_within_5kb_hot += 1
            if within_10kb_hot >= 1:
                total_within_10kb_hot += 1
            if within_20kb_hot >= 1:
                total_within_20kb_hot += 1
            z += 1
            within_hotspot = 0
            within_1kb_hot = 0
            within_2kb_hot = 0
            within_5kb_hot = 0
            within_10kb_hot = 0
            within_20kb_hot = 0
        #summary
        summary = "Summary\n\n Total hotspots within contig boundaries: %s\n Total hotspots within 1kb of contig boundaries: %s\n Total hotspots within 2kb of contig boundaries: %s\n Total hotspots within 5kb of contig boundaries: %s\n Total hotspots within 10kb of contig boundaries: %s\n Total hotspots within 20kb of contig boundaries: %s\n" % (total_within_hot, total_within_1kb_hot, total_within_2kb_hot, total_within_5kb_hot, total_within_10kb_hot, total_within_20kb_hot)
        out.write(summary)

compare()
