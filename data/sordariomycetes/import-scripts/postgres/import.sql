/* Make sure to remove the first lines (with field names) from the txt files before importing! */

COPY "@TABLEPREFIX@taxon" FROM '@BASEPATH@taxa.txt' NULL AS '';
COPY "@TABLEPREFIX@distribution" FROM '@BASEPATH@distribution.txt' NULL AS '';
COPY "@TABLEPREFIX@description" FROM '@BASEPATH@description.txt' NULL AS '';
COPY "@TABLEPREFIX@reference" FROM '@BASEPATH@reference.txt' NULL AS '';
COPY "@TABLEPREFIX@vernacular" FROM '@BASEPATH@vernacular.txt' NULL AS '';