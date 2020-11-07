/* Example of how to import Spotify data into Stata
 * Author: Sophia Hadash (s.hadash@tue.nl) */

 
// 1. EDIT THESE LINES -------------------------------------

// change working directory
cd "C:\Users\s125810\Desktop\Spotify sample data\mysqldump"

// specify which file to load
local f "tracks.txt"

//----------------------------------------------------------

// import a file
import delimited `f', clear


// 2. PRE PROCESSING -------------------------------------

/* Now the file is imported, but column names are missing
 proceed with pre-processing. There is a file with the same name but extension *.sql
 consult this file. In this example, this is tracks.sql
 
 This file contains the following contents with information on the data:
 
 ### FILE: tracks.sql #############################################################
--
-- Table structure for table `tracks`
--

DROP TABLE IF EXISTS `tracks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(24) NOT NULL,
  `name` text NOT NULL,
  `popularity` int(11) NOT NULL,
  `preview` text NOT NULL,
  `uri` text NOT NULL,
  `is_local` int(11) NOT NULL,
  `is_playable` int(11) NOT NULL,
  `external_url` text NOT NULL,
  `href` text NOT NULL,
  `duration_ms` int(11) NOT NULL,
  `artists` text NOT NULL,
  `album_id` text NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `track_id` (`track_id`)
) ENGINE=MyISAM AUTO_INCREMENT=622187 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
###################################################################################

Look at the table structure to identify the variable types. These are some quick field explanations:

varchar -> a text field
int -> a number
boolean -> either one or zero
datetime -> a date or time
set -> a set of options, like a categorical variable with labels */

//rename the columns
rename v1 id
rename v2 track_id
rename v3 name
rename v4 popularity
rename v5 preview
rename v6 uri
rename v7 is_local
rename v8 is_playable
rename v9 external_url
rename v10 href
rename v11 duration_ms
rename v12 artists
rename v13 album_id
rename v14 timestamp
