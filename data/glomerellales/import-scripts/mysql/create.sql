DROP TABLE IF EXISTS `@TABLEPREFIX@taxon`;
DROP TABLE IF EXISTS `@TABLEPREFIX@distribution`;
DROP TABLE IF EXISTS `@TABLEPREFIX@vernacular`;
DROP TABLE IF EXISTS `@TABLEPREFIX@reference`;

CREATE TABLE `@TABLEPREFIX@taxon` (
  `taxonID` int NOT NULL,
  `identifier` varchar(255) default NULL,
  `datasetID` varchar(255) default NULL,
  `datasetName` varchar(255) default NULL,
  `acceptedNameUsageID` int default NULL,
  `parentNameUsageID` int default NULL,
  `taxonomicStatus` varchar(255) default NULL,
  `taxonRank` varchar(255) default NULL,
  `verbatimTaxonRank` varchar(255) default NULL,
  `scientificName` varchar(255) default NULL,
  `kingdom` varchar(255) default NULL,
  `phylum` varchar(255) default NULL,
  `class` varchar(255) default NULL,
  `order` varchar(255) default NULL,
  `superfamily` varchar(255) default NULL,
  `family` varchar(255) default NULL,
  `genericName` varchar(255) default NULL,
  `genus` varchar(255) default NULL,
  `subgenus` varchar(255) default NULL,
  `specificEpithet` varchar(255) default NULL,
  `infraspecificEpithet` varchar(255) default NULL,
  `scientificNameAuthorship` varchar(255) default NULL,
  `source` text,
  `namePublishedIn` text,
  `nameAccordingTo` varchar(255) default NULL,
  `modified` varchar(255) default NULL,
  `description` text,
  `taxonConceptID` varchar(255) default NULL,
  `scientificNameID` varchar(255) default NULL,
  `references` varchar(255) default NULL,
  `isExtinct` varchar(10) default NULL,
  PRIMARY KEY  (`taxonID`)
);

CREATE TABLE `@TABLEPREFIX@distribution` (
  `taxonID` int NOT NULL,
  `locationID` varchar(255) default NULL,
  `locality` text,
  `occurrenceStatus` varchar(255) default NULL,
  `establishmentMeans` varchar(255) default NULL
);

CREATE TABLE `@TABLEPREFIX@description` (
  `taxonID` int NOT NULL,
  `description` text
);

CREATE TABLE `@TABLEPREFIX@reference` (
  `taxonID` int NOT NULL,
  `creator` varchar(255) default NULL,
  `date` varchar(255) default NULL,
  `title` varchar(255) default NULL,
  `description` text,
  `identifier` varchar(255) default NULL,
  `type` varchar(255) default NULL
);

CREATE TABLE `@TABLEPREFIX@vernacular` (
  `taxonID` int NOT NULL,
  `vernacularName` varchar(255) NULL,
  `language` varchar(255) NULL,
  `countryCode` varchar(255) NULL,
  `locality` varchar(255) NULL,
  `transliteration` varchar(255) NULL
);
