# NYC Job Postings Analysis (Jan 2025 – Feb 2026)

The goal of this project is to analyze job postings on the official NYC job site to uncover hiring trends, salary distributions, in-demand skills across agencies, and better understand the NYC job market.  

I chose this project because I am interested in exploring which jobs are high paying, the availability of different positions, and which skills are currently in high demand.

## Dataset
The original dataset (15.4MB) can be downloaded [here](https://catalog.data.gov/dataset/nyc-jobs) as of March 19, 2026.  
The cleaned version is available as `nyc_jobs_cleaned.csv`.  

The dataset includes fields such as job title, agency, salary range (from/to), posting dates, preferred skills, and more.

## Research Questions
* How have NYC job postings changed over time?
* Which agencies offers the highest median salaries?
* Among agencies with significant hiring activity, do those that post more jobs offer lower salaries?
* What are the most frequently occurring skills or keywords in job descriptions?
* Which kind of job titles are most frequently posted?
* Which agencies hire the most data related roles?

## Tools and Technologies

* **SQL:** Used to remove duplicate job entries, convert hourly/daily salaries to annual salaries, calculate mean salary from the salary range (`Salary Range From` and `Salary Range To`), and keep only relevant fields for analysis.
```sql
-- Delete Duplicate Jobs
DELETE FROM nyc_jobs
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM nyc_jobs
    GROUP BY "Job ID"
);
```
* Python: Using Pandas to perform aggregation, text analysis, custom filtering using regex-based cleaning, correlation analysis, data cleaning and processing, and time series analysis

**Example: Identifying data related roles using keyword based filtering**
```python
# Identify data related roles using keywords
title_keywords = "data|machine learning|business intelligence|data analysis"
skill_keywords = "python|sql|tableau|power bi|pandas"

title_mask = df["Civil Service Title"].str.contains(title_keywords, case=False, na=False)
skill_mask = df["Preferred Skills"].str.contains(skill_keywords, case=False, na=False)

data_roles = title_mask | skill_mask 

# Count data related roles by agency
data_roles_by_agency = (
    data_roles.groupby("Agency")
    .size()
    .reset_index(name="Count")
    .head(10)
)
```

* Power BI: Used for dashboard creation and visualization



## Insights

* **Job posting trends:**  
  - Jan–Sep 2025: relatively low, averaging 9.6 postings/month (except June: 70 postings)  
  - Oct 2025: 170 postings  
  - Nov 2025: 279 postings  
  - Dec 2025: 907 postings  
  - Jan 2026: 1,301 postings (peak)  
  - Feb 2026: 38 postings  

  This suggests seasonal recruitment patterns or usage of remaining budget funds.

* **Top five agencies by median salary** (only agencies with ≥3 postings):  
  - **Financial Information Services Agency** – $132,000  
  - **Law Department** – $131,000  
  - **NYC Employees’ Retirement System** – $130,000  
  - **Conflicts of Interest Board** – $125,000  
  - **Office of Criminal Justice** – $119,000
    
  Note: Only agencies with at least 3 job postings were included because agencies with low postings (e.g., agencies with only 1 posting) may not accurately reflect typical salaries. 

* **Correlation between postings and salary:**  
There is no significant correlation (r = -0.0475).  
![Correlation Plot](https://raw.githubusercontent.com/xiaojie10/nyc_job_postings_analysis/main/Data/correlation.png)

* **Most frequent preferred skills:**  
  Microsoft Word, Excel, driver's license, written/communication skills, ENV SP certification, project management, Primavera P6.

* **Top five jobs by number of postings:**  
  - Community Coordinator – 107  
  - Community Associate – 92  
  - City Research Scientist – 62  
  - Principal Administrative Associate – 50  
  - Agency Attorney – 43

* **Top agencies hiring data-related roles:**  
  - Dept. of Design & Construction – 15 postings  
  - Dept. of City Planning – 7 postings  
  - Bronx District Attorney – 4 postings

### Dashboard Overview

**Dashboard 1:** 
![Dashboard 1](https://raw.githubusercontent.com/xiaojie10/nyc_job_postings_analysis/main/Data/dashboard1.png)

**Dashboard 2:** 
![Dashboard 2](https://raw.githubusercontent.com/xiaojie10/nyc_job_postings_analysis/main/Data/dashboard2.png)

**Dashboard 3:**  
![Dashboard 3](https://raw.githubusercontent.com/xiaojie10/nyc_job_postings_analysis/main/Data/dashboard3.png)

