-- Modify if you want the table names to have a prefix:
DECLARE @table_prefix VARCHAR(16) = '';

-- Create table Taxon
EXEC('
	CREATE TABLE "' + @table_prefix + 'Taxon" (
	  "taxonID" int NOT NULL,
	  "identifier" varchar(255) default NULL,
	  "datasetID" varchar(255) default NULL,
	  "datasetName" varchar(255) default NULL,
	  "acceptedNameUsageID" int default NULL,
	  "parentNameUsageID" int default NULL,
	  "taxonomicStatus" varchar(255) default NULL,
	  "taxonRank" varchar(255) default NULL,
	  "verbatimTaxonRank" varchar(255) default NULL,
	  "scientificName" varchar(255) default NULL,
	  "kingdom" varchar(255) default NULL,
	  "phylum" varchar(255) default NULL,
	  "class" varchar(255) default NULL,
	  "order" varchar(255) default NULL,
	  "superfamily" varchar(255) default NULL,
	  "family" varchar(255) default NULL,
	  "genericName" varchar(255) default NULL,
	  "genus" varchar(255) default NULL,
	  "subgenus" varchar(255) default NULL,
	  "specificEpithet" varchar(255) default NULL,
	  "infraspecificEpithet" varchar(255) default NULL,
	  "scientificNameAuthorship" varchar(255) default NULL,
	  "source" text,
	  "namePublishedIn" text,
	  "nameAccordingTo" varchar(255) default NULL,
	  "modified" varchar(255) default NULL,
	  "description" text,
	  "taxonConceptID" varchar(255) default NULL,
	  "scientificNameID" varchar(255) default NULL,
	  "references" varchar(255) default NULL,
	  "isExtinct" varchar(10) default NULL,
	  PRIMARY KEY  ("taxonID")
	);
');


-- Create table Distribution
EXEC('
	CREATE TABLE "' + @table_prefix + 'Distribution" (
	  "taxonID" int NOT NULL,
	  "locationID" varchar(255) default NULL,
	  "locality" text,
	  "occurrenceStatus" varchar(255) default NULL,
	  "establishmentMeans" varchar(255) default NULL
	);
');

-- Create table Description
EXEC('
	CREATE TABLE "' + @table_prefix + 'Description" (
	  "taxonID" int NOT NULL,
	  "description" text
	);
');

-- Create table Reference
EXEC('
	CREATE TABLE "' + @table_prefix + 'Reference" (
	  "taxonID" int NOT NULL,
	  "creator" varchar(255) default NULL,
	  "date" varchar(255) default NULL,
	  "title" varchar(255) default NULL,
	  "description" text,
	  "identifier" varchar(255) default NULL,
	  "type" varchar(255) default NULL
	);
');


-- Create table VernacularName
EXEC('
	CREATE TABLE "' + @table_prefix + 'VernacularName" (
	  "taxonID" int NULL,
	  "vernacularName" varchar(255) NULL,
	  "language" varchar(255) NULL,
	  "countryCode" varchar(255) NULL,
	  "locality" varchar(255) NULL,
	  "transliteration" varchar(255) NULL
	);
');

