#Identifying contig boundaries

#step 1
samtools mpileup <reference file> <sorted and filtered bam file> >> <output.mpileup file>

#step 2
#command from http://www.biostars.org/p/12028/
#Question: How to Get All Contig Boundaries in bam file
#-d ' ' where '' is the delimiter of the file, in my case a tab (\t)
cut -d '  ' -f 1,2 <mpileup file> | awk 'BEGIN {chr="";start=-1;end=-1} {if(chr!=$1 || int ($2) !=end+1) {if (chr!="")} {printf ("%s:%d-%d\n",chr,start,end);} chr=$1;start=int($2);end=int($2);} else { end=end+1;}} END {if (chr!="") {printf ("%s:%d-%d\n",chr,start,end);} }'
