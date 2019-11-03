#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob,os


# In[2]:


"""
Summary:  
This function cleans the financial metrics data scraped online.
Add 'year' and 'quarter' column to each quarter's financial data; 
Concat the financial datasets from each quarter; 
Rename the unnamed columns;
Calculate the 'Expense' of each company by summing up R&D, SG&A, Operating, Interest and Income Tax expenses; 
extract the useful columns: company name, year, quarter, revenue, expenses, EBITDA
Remove the data points with missing financial metrics values 

Returns:
Final financial dataframe with fiancial metrics data: Company name, Year, Quarter, Revenue, Expenses, EBITDA

NOTE: 
All the financial data should be organized by year and quarter, and named in the format 'year_quarter.csv'.No other csv 
file should be in the working directory.  
"""
def FinancialClean(filelocation):
    
    if (filelocation == None):
      raise ValueError('Filelocation is mandatory')
    else:
        df_list = []
        all_files = glob.glob(os.path.join(filelocation, "*.csv"))  
        for file in all_files:
            year = file.split('/')[-1].split('_')[0] 
            quarter = file.split('/')[-1].split('_')[1].split('.')[0]
            df = (pd.read_csv(file)
                    .assign(Year = year, Quarter = quarter))
            df_list.append(df)
       
        financial1= pd.concat(df_list)
        
        financial1.rename(columns={'Unnamed: 0':'CompanyName'}, inplace=True)
        expense_cols = [col for col in financial1.columns if 'Expense' in col]
        financial1['Expense'] = financial1[expense_cols].sum(axis=1)
        financial1 = financial1[['CompanyName', 'Year', 'Quarter', 'Revenue', 'Expense', 'EBITDA']]
        financial = financial1.dropna(subset=['Revenue','Expense','EBITDA'])
        
        return(financial)


    


# In[3]:


#test with sample data and write to csv
mylocation = '/Users/tanduyun/Desktop/MSiA 400 everything starts with data/fdata'
financial = FinancialClean(mylocation)
financial.to_csv("FinancialData.csv", index= False)


# In[4]:


financial


# In[ ]:




