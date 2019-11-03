import pandas as pd

def extract_posting_counts(file):
    postings = pd.read_csv(file, encoding = "ISO-8859-1")
    postings['year'] = pd.DatetimeIndex(postings['post_date']).year #extracts the year from the post date and stores as a separate column
    postings['month'] = pd.DatetimeIndex(postings['post_date']).month #extracts the month from the post date
    
    quarter = list() #creates a separate list for quarter
    q1 = (1, 2, 3)
    q2 = (4, 5, 6)
    q3 = (7, 8, 9)
    q4 = (10, 11, 12)

    for i in postings['month']:
        if i in q1:
            quarter.append("Q1")
        elif i in q2:
            quarter.append("Q2")
        elif i in q3:
            quarter.append("Q3")
        else:
            quarter.append("Q4")
        
    postings['quarter'] = quarter
    
    postcols = postings[['quarter', 'year', 'ticker']] #creates a subset of the quarter, year, and company of the posting
    postcounts = postcols.groupby(['quarter', 'year'])['ticker'].value_counts().to_frame('postings') #counts the posting per quarter and stores as a new column in the data frame
    
    postcounts.to_csv("postcounts.csv")
