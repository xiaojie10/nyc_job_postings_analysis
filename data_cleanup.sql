-- Delete Dupplicate Jobs
DELETE FROM nyc_jobs
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM nyc_jobs
    GROUP BY "Job ID"
);


-- Displaying releveant fields only, converting houly salries to annual salary then conclude its mean salary by finding the mean between the salary ranges
WITH cal_salary AS(
SELECT
	Agency,
	"# Of Positions", 
	"Civil Service Title", 
	"Posting Date", 
	"Post Until",
	"Preferred Skills",
	"Salary Range From",
	"Salary Range To",
CASE
	WHEN "Salary Frequency" =  "Hourly" THEN "Salary Range From" * 40 * 52
	WHEN "Salary Frequency" = 'Daily' THEN "Salary Range From" * 5 * 52
	ELSE "Salary Range From"
END AS salary_from_annual,
CASE
	WHEN "Salary Frequency" =  "Hourly" THEN "Salary Range To" * 40 * 52
	WHEN "Salary Frequency" = 'Daily' THEN "Salary Range To" * 5 * 52
	ELSE "Salary Range To"
END AS salary_to_annual
FROM nyc_jobs
)
SELECT 
	Agency,
	"# Of Positions", 
	"Civil Service Title", 
	"Posting Date", 
	"Preferred Skills",
	"salary_from_annual" AS "Salary Range From (Annual)" ,
	"salary_to_annual" AS "Salary Range To (Annual)",
	(salary_from_annual + salary_to_annual) / 2 AS mean_annual_salary
FROM cal_salary


