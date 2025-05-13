USE ROLE ACCOUNTADMIN;
USE WAREHOUSE HOUSING_MARKET_WH;

CREATE OR REPLACE DATABASE US_HOUSING_MARKET;
CREATE OR REPLACE SCHEMA CENSUS_DATA;

USE DATABASE US_HOUSING_MARKET;
USE SCHEMA CENSUS_DATA;
CREATE OR ALTER STAGE CENSUS_STAGE;

CREATE OR REPLACE FILE FORMAT CENSUS_STAGE_JSON TYPE = 'JSON';

---> Changing CENSUS_STAGE format to match the CENSUS_STAGE_JSON JSON format,View the RAW data in the staged JSON files
SELECT $1 FROM 
@CENSUS_STAGE (file_format=>'CENSUS_STAGE_JSON',pattern=> '.*.*');

---> Flatten the JSON structure in to a tabular format and access it as a view
---> UPDATE ** MAKE SURE TO ADD YEAR in View

CREATE OR REPLACE VIEW CENSUS_STAGE_VIEW AS 
SELECT 
    t.value:"NAME"::string AS name,
    t.value:"B01001_001E"::integer AS total_population,
    t.value:"B01001_002E"::integer AS male_population,
    t.value:"B01001_026E"::integer AS female_population,
    t.value:"B02001_002E"::integer AS white_population,
    t.value:"B02001_003E"::integer AS black_population,
    t.value:"B02001_004E"::integer AS native_american_population,
    t.value:"B02001_005E"::integer AS asian_population,
    t.value:"B02001_006E"::integer AS pacific_islander_population,
    t.value:"B02001_007E"::integer AS other_population,
    t.value:"B02001_008E"::integer AS hispanic_population,
    t.value:"B19013_001E"::integer AS median_income,
    t.value:"state"::string AS state_code,
    t.value:"place"::string AS place_code,
    t.value:"year"::integer AS year
FROM 
@CENSUS_STAGE (file_format => 'CENSUS_STAGE_JSON', pattern => '.*.*') AS S,
    LATERAL FLATTEN (input => S.$1) t;
