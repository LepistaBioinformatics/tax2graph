-- Modify as appropriate for your own situation. Enter
-- the directory containing the darwin core archive files
-- (taxa.txt, distribution.txt, etc.). The path must end
-- with a backslash.
DECLARE @export_dir VARCHAR(100) = 'C:\Users\Ayco Holleman\Downloads\dca01\';

-- Modify if you want the table names to have a prefix:
DECLARE @table_prefix VARCHAR(16) = '';



EXEC('TRUNCATE TABLE ' + @table_prefix + 'Taxon');
EXEC('TRUNCATE TABLE ' + @table_prefix + 'Distribution');
EXEC('TRUNCATE TABLE ' + @table_prefix + 'Description');
EXEC('TRUNCATE TABLE ' + @table_prefix + 'Reference');
EXEC('TRUNCATE TABLE ' + @table_prefix + 'VernacularName');



DECLARE @bulk_cmd varchar(1000);

SET @bulk_cmd = 'BULK INSERT ' + @table_prefix + 'Taxon
FROM ''' + @export_dir + 'taxa.txt''
WITH (FIRSTROW = 2, FIELDTERMINATOR = ''' + CHAR(9) + ''', ROWTERMINATOR = ''' + CHAR(10)+ ''')';

EXEC(@bulk_cmd);


SET @bulk_cmd = 'BULK INSERT ' + @table_prefix + 'Distribution
FROM ''' + @export_dir + 'distribution.txt''
WITH (FIRSTROW = 2, FIELDTERMINATOR = ''' + CHAR(9) + ''', ROWTERMINATOR = ''' + CHAR(10)+ ''')';

EXEC(@bulk_cmd);


SET @bulk_cmd = 'BULK INSERT ' + @table_prefix + 'Description
FROM ''' + @export_dir + 'description.txt''
WITH (FIRSTROW = 2, FIELDTERMINATOR = ''' + CHAR(9) + ''', ROWTERMINATOR = ''' + CHAR(10)+ ''')';

EXEC(@bulk_cmd);


SET @bulk_cmd = 'BULK INSERT ' + @table_prefix + 'VernacularName
FROM ''' + @export_dir + 'vernacular.txt''
WITH (FIRSTROW = 2, FIELDTERMINATOR = ''' + CHAR(9) + ''', ROWTERMINATOR = ''' + CHAR(10)+ ''')';

EXEC(@bulk_cmd);


SET @bulk_cmd = 'BULK INSERT ' + @table_prefix + 'Reference
FROM ''' + @export_dir + 'reference.txt''
WITH (FIRSTROW = 2, FIELDTERMINATOR = ''' + CHAR(9) + ''', ROWTERMINATOR = ''' + CHAR(10)+ ''')';

EXEC(@bulk_cmd);