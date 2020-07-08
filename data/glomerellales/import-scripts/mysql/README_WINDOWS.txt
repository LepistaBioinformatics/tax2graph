=================================================================
====               MySQL import scripts                      ====
====               for Catalogue of Life                     ====
====           Darwin Core Archive Downloads                 ====
=================================================================

Author: Ayco Holleman
Copyright: ETI BioInformatics
Developed in: i4Life project Work Package 4
Version 1.0, 2012



Synopsis
=================================================================
The import_windows.bat script will help you import files generated
by the Darwin Core Archive (DWC-A) download service into MySQL.
create.sql and import.sql are helper scripts, used by import_windows.bat.



Usage
=================================================================

CMD> import_windows -u user -d database [-h host] [-p password] [-e exportdir] [-x prefix] [-n]

Command line arguments:

	-u	The MySQL database user
	-d	The MySQL database into which to import the data
	-h	The MySQL server host (default: localhost)
	-p	The MySQL password (default: none)
	-e	The directory containing the DCA export files (default: present
				working directory)
	-x 	The table prefix to be used when creating and loading the
				tables (default: none). If you want to import the DCA data
				into a pre-existent database, you might want to specify a 
				table prefix
	-n 	Skip table creation (only load data)
					



N.B. you MUST run import_windows.bat from within the directory that contains it. In
other words, you must first change directory to import-scripts/mysql.



