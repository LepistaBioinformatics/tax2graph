REM #################################################################
REM ##  Author: Ayco Holleman                                      ##
REM ##  Copyright: ETI BioInformatics                              ##
REM ##  Developed in: i4Life project Work Package 4                ##
REM ##  Version 1.0, 2012                                          ##
REM #################################################################

@ECHO off
TITLE DWC-A Import
CLS

SET script=%0
SET tmpdir=C:\Windows\Temp\

REM Check environment
CALL psql --version >NUL 2>NUL
IF errorlevel 1 (	
	ECHO PostgreSQL command line client not found.
	EXIT /B 1
)



REM Initialize vars
SET host=localhost
SET user=
SET password=
SET database=
SET exportdir=
SET prefix=
SET nocreate=false



REM Set vars from command line
:begin_parse_args
IF "%1"=="" GOTO end_parse_args
IF "%1"=="-h" (
	SET host=%2
	SHIFT
)	
IF "%1"=="-u" (
	SET user=%2
	SHIFT
)	
IF "%1"=="-p" (
	SET password=%2
	SHIFT
)	
IF "%1"=="-d" (
	SET database=%2
	SHIFT
)	
IF "%1"=="-e" (
	SET exportdir=%2
	SHIFT
)	
IF "%1"=="-x" (
	SET prefix=%2
	SHIFT
)	
IF "%1"=="-n" (
	SET nocreate=true
)	
SHIFT	
GOTO begin_parse_args
:end_parse_args


REM Check user input
IF "%user%"=="" (
	call:usage User not specified
	EXIT /B 1
)
IF "%database%"=="" (
	call:usage Database not specified
	EXIT /B 1
)
IF "%exportdir%"=="" (
	call:usage DWC-A export directory not specified
	EXIT /B 1
)
IF NOT EXIST %exportdir% (
	ECHO No such directory: %exportdir%
	EXIT /B 1
)
IF NOT EXIST %exportdir%/taxa.txt (
	ECHO Directory does not seem to be a DCA export directory: "%exportdir%"
	EXIT /B 1
)

REM Make sure we can connect to PostgreSQL
IF "%password%=="" (
	ECHO \q | psql -q --host %host% --username %user% --dbname %database%
) ELSE (
	ECHO \q | psql -q --host %host% --username %user% --dbname %database% --password %password%
)
IF errorlevel 1 (
	ECHO Cannot connect to PostgreSQL using the specified connection parameters
	EXIT /B 1
)

REM Replace backward slashes in export dir with forward slashes,
REM otherwise psql will choke. Also make sure export dir ends
REM with forward slash
SET exportdir=%exportdir:\=/%/



REM Create tables, unless user specified otherwise
IF %nocreate%==false (
	COPY create.sql %tmpdir%create.tmp.sql >NUL
	call:find_replace %tmpdir%create.tmp.sql @TABLEPREFIX@ %prefix%
	TYPE %tmpdir%create.tmp.sql | call:my_psql
	IF "%password%=="" (
		TYPE %tmpdir%create.tmp.sql | psql -q --host %host% --username %user% --dbname %database%
	) ELSE (
		TYPE %tmpdir%create.tmp.sql | psql -q --host %host% --username %user% --dbname %database% --password %password%
	)
	DEL %tmpdir%create.tmp.sql
)

REM Import data
COPY import.sql %tmpdir%import.tmp.sql >NUL
call:find_replace %tmpdir%import.tmp.sql @TABLEPREFIX@ %prefix%
call:find_replace %tmpdir%import.tmp.sql @BASEPATH@ %exportdir%
IF "%password%=="" (
	TYPE %tmpdir%import.tmp.sql | psql -q --host %host% --username %user% --dbname %database%
) ELSE (
	TYPE %tmpdir%import.tmp.sql | psql -q --host %host% --username %user% --dbname %database% --password %password%
)
DEL %tmpdir%import.tmp.sql


ECHO Import complete

REM end of main
GOTO:EOF

REM Debug function
:var_dump
	ECHO host ..........: %host%
	ECHO user ..........: %user%
	ECHO password ......: %password%
	ECHO database ......: %database%
	ECHO export dir ....: %exportdir%
	ECHO table prefix ..: %prefix%
	ECHO import only ...: %nocreate%
GOTO:EOF

:usage
	ECHO USAGE: %script% -u user -d database [-h host] [-p password] [-x prefix] [-e exportdir] [-n]
	ECHO %*
GOTO:EOF

:find_replace
	cscript //nologo replaceText.vbs %1 %2 %3
GOTO:EOF


