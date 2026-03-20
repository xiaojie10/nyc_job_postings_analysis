import pandas as pd
import sqlite3
from collections import Counter
import re

conn = sqlite3.connect("Data/jobs.db")

query = """
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
	WHEN "Salary Frequency" =  'Hourly' THEN "Salary Range From" * 40 * 52
	WHEN "Salary Frequency" = 'Daily' THEN "Salary Range From" * 5 * 52
	ELSE "Salary Range From"
END AS salary_from_annual,
CASE
	WHEN "Salary Frequency" =  'Hourly' THEN "Salary Range To" * 40 * 52
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
	salary_from_annual AS "Salary Range From (Annual)" ,
	salary_to_annual AS "Salary Range To (Annual)",
	(salary_from_annual + salary_to_annual) / 2 AS "Mean Annual Salary"
FROM cal_salary
"""

df = pd.read_sql_query(query, conn)
df["Posting Date"] = pd.to_datetime(df["Posting Date"])

# Convert the salaries into whole numbers
salary_columns = ["Salary Range From (Annual)", "Salary Range To (Annual)", "Mean Annual Salary" ]
df[salary_columns] = df[salary_columns].round().astype(int)

# Find the agencies with the highest median salary with at least 3 job postings
def agency_median_salary(df):
    result = (
        df.groupby("Agency")["Mean Annual Salary"]
        .agg(["median", "count"])
        .query("count >= 3")
        .sort_values("median", ascending = False)
        .reset_index()
    )
    
    result["median"] = result["median"].round().astype(int)
    return result

# Returns the top 20 most posted job titles
def frequently_posted_jobs(df):
    return df["Civil Service Title"].value_counts().head(20).reset_index()

# Return the top 20 hiring agencies
def top_agency_hiring(df):
    return df.groupby("Agency")["# Of Positions"].sum().sort_values(ascending = False).reset_index().head(20)

# Finds the agency with the most data related job titles using keywords and title filtering
def agency_data_hire(df):
    title_keywords = "data analysis|data scientist|machine learning|business intelligence|data engineer|data science"
    skill_keywords = "power bi|tableau|sql|python|pandas|data visualization|r programming|numpy|machine learning"

    title_mask = df['Civil Service Title'].str.contains(title_keywords, case=False, na=False)
    skill_mask = df["Preferred Skills"].str.contains(skill_keywords, case=False, na=False)

    combine_mask = title_mask | skill_mask

    results = df.loc[combine_mask, ['Agency', 'Civil Service Title']]

    # Agencies with their respective data related titles
    grouped_with_titles = (
        results
        .groupby(["Agency", "Civil Service Title"])
        .size()
        .reset_index(name="Count")
    )

    # Agencies with their count of data related titles
    agency_totals = (
        grouped_with_titles
        .groupby("Agency")["Count"]
        .sum()
        .reset_index()
        .sort_values("Count", ascending=False)
    )

    return agency_totals


# Finds the number of job postings per month and by year
def job_posting_change(df, year):
    df["Posting Date"] = pd.to_datetime(df["Posting Date"])
    df_year = df.loc[df["Posting Date"].dt.year == year]
    postings_per_month_by_year = df_year.groupby(df_year["Posting Date"].dt.month_name())["# Of Positions"].sum()

    postings_per_month_by_year = postings_per_month_by_year.reset_index()
    return postings_per_month_by_year


# Returns the most frequent skill 
def find_frequent_skills(df):
    junk_words = {
        "the","a","an","and","of","to","in","for","with","is","are",
        "must","should","will","such","as","skills","position","at",
        "following","new","york","years","experience","note","ability",
        "this","preferred","candidate","role","responsibilities","required",
        "working","knowledge","professional","including","have","valid",
        "please","department","office","city","nyc","current", 
        "specifications","dep","dot", "nys", "mutcd","aashto", "sustainability", "envision",
        "comprehensive", "proficiency", "outstanding","standards",
        "0","1","2","3","4","5","6","7","8","9"
    }

    # Remove missing values
    skill_descriptions = df["Preferred Skills"].dropna()
    
    cleaned_skill_description = []

    # Loop through each description, create bigrams, and remove junk words from description
    for desc in skill_descriptions: 
        desc = desc.lower()
        desc = re.sub(r'[^a-z0-9\s]', '', desc)
        words = desc.split()
        
        clean_words = []
        for word in words:
            if word not in junk_words:
                clean_words.append(word)
        
        cleaned_skill_description.append(clean_words)

    # Generate bigrams using zip
    all_bigrams = []
    for words in cleaned_skill_description:
        bigrams = zip(words, words[1:])
        for bigram in bigrams:
            all_bigrams.append(bigram)

    # Count bigrams
    bigram_counts = Counter(all_bigrams).most_common(25)
    
    # Convert to string to be more readable
    bigram_strings = [f"{w1} {w2}: {count}" for (w1, w2), count in bigram_counts]

    return bigram_strings

# Gets the correlation between salary and number of positions
def salary_correlation(df):
    correlation_df = (
        df.groupby("Agency")
        .agg({"# Of Positions": "sum", "Mean Annual Salary": "mean"})
        .sort_values("# Of Positions", ascending=False)
        .head(50)
        .reset_index()
    )

    correlation_df["Mean Annual Salary"] = correlation_df["Mean Annual Salary"].round().astype(int) 

    # Gets the correlation r 
    correlation = correlation_df["# Of Positions"].corr(correlation_df["Mean Annual Salary"])
    
    return correlation_df, correlation

