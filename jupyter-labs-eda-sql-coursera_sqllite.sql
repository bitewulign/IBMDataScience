-- CREATE DATABASE ibmdatabase
USE ibmdatabase;
-- download Table https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv
-- right click the created ibmdatabase and Table Data Import Wizard
-- follow the prompts
SHOW TABLES;
SELECT * FROM spacex;

-- Task 1
-- Display the names of the unique launch sites in the space mission
SELECT DISTINCT LAUNCH_SITE FROM spacex;

-- Task 2
-- Display 5 records where launch sites begin with the string 'CCA'
SELECT * FROM spacex WHERE Launch_Site LIKE 'CCA%' LIMIT 5;

-- Task 3
-- Display the total payload mass carried by boosters launched by NASA (CRS)
SELECT SUM(PAYLOAD_MASS__KG_) AS TotalPayLoadMass FROM spacex WHERE Customer = 'NASA (CRS)';

-- Task 4
-- Display average payload mass carried by booster version F9 v1.1
SELECT AVG(PAYLOAD_MASS__KG_) AS AveragePayLoadMass FROM spacex WHERE Booster_Version = 'F9 v1.1';

-- Task 5
-- List the date when the first succesful landing outcome in ground pad was acheived.
SELECT MIN(Date) AS FirstSuccessfulGroundPadLandingDate 
FROM spacex
WHERE Landing_Outcome ='Success (ground pad)';

-- Task 6
-- List the names of the boosters which have success in drone ship 
-- and have payload massgreater than 4000 but less than 6000
SELECT Booster_Version      
FROM spacex
WHERE Landing_Outcome = 'Success (Drone Ship)'
And PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;

-- Task 7
-- List the total number of successfull and failur mission outcomes
SELECT Mission_Outcome, COUNT(*) AS OutcomeCount
FROM spacex
WHERE Mission_Outcome IN ('Success', 'Failure')
GROUP BY Mission_Outcome;

-- Task 8
-- List the names of the booster_versions which have carried the maximum payload mass. Use a subquery.
SELECT Booster_Version
FROM spacex
WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM spacex);

-- Task 9
-- List the records which will display the month names, 
-- failure landing_outcomes in drone ship ,booster versions, 
-- launch_site for the months in year 2015.
-- Note: SQLLite does not support monthnames. 
-- So you need to use  substr(Date, 6,2) as month to get the months 
-- and substr(Date,0,5)='2015' for year.
SELECT SUBSTR(DATE, 6, 2) AS Month, CASE
WHEN Landing_Outcome = 'Failure (drone ship)' 
THEN 'Failure' End As Landing_Outcome, Booster_Version, Launch_Site
FROM spacex
WHERE SUBSTR(DATE, 1,4) = '2015';

-- Task 10
-- Rank the count of landing outcomes (such as Failure (drone ship) or 
-- Success (ground pad)) between the date 2010-06-04 and 2017-03-20, 
-- in descending order.
SELECT Landing_Outcome, COUNT(*) AS OutcomeCount
FROM spacex
WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY Landing_Outcome
ORDER BY OutcomeCount DESC;

-- Reference 
/* */
-- Author: Bitewulign Kassa 
-- February 19, 2024