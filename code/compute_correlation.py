#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import pearsonr


# In[2]:


# define a function that merges the financial data with job posting data by company and quarter
def MergeFinancialPostings(FinancialData, PostingsData):
    # rename the columns and set indices for data frames
    FinancialData = FinancialData.rename(columns = {"CompanyName":"Company"}).set_index(["Year", 'Quarter', 'Company'])
    PostingsData = PostingsData.rename(columns = {"year":"Year","quarter":"Quarter","ticker":"Company","postings":"NumberOfPosts"}).set_index(["Year", 'Quarter', 'Company'])
    
    # merge financial data and the number of posts for each company in the corresponding quarter
    FinancialPostsData = FinancialData.join(PostingsData)
    return(FinancialPostsData)


# In[3]:


# define a function that prints the scatterplots among financial and posting metrics
def ScatterPlot(FinancialPostsData):
    pd.scatter_matrix(FinancialPostsData, figsize=(6, 6))
    plt.show()
    
# define a function that calculates the correlation between the financial and posting metrics
def ComputeCorrelation(FinancialPostsData):
    corrMatrix = FinancialPostsData.corr()
    print(corrMatrix)
    
# define a function that prints the scatterplots among financial and posting metrics
def HeatMap(FinancialPostsData):
    corrMatrix = FinancialPostsData.corr()
    f, ax = plt.subplots(figsize =(9, 8)) 
    sns.heatmap(corrMatrix, ax = ax, cmap ="YlGnBu", linewidths = 0.1) 

# define a function that conducts Pearson tests on the correlations
def CorrTest(FinancialPostsData):
    # extract the variables from the data frame
    Revenue = FinancialPostsData['Revenue'].values
    Expense = FinancialPostsData['Expense'].values
    EBITDA = FinancialPostsData['EBITDA'].values
    NumberOfPosts = FinancialPostsData['NumberOfPosts'].values
    
    # remove NaN values and conduct Pearson's test between revenue and the number of posts
    bad = ~np.logical_or(np.isnan(Revenue), np.isnan(NumberOfPosts))
    corr, p_value = pearsonr(np.compress(bad, Revenue), np.compress(bad, NumberOfPosts))
    print("The correlation between revenue and the number of posts is ", corr, 
      ", and the p-value for Pearson's test is ", p_value, sep = '')
    
    # remove NaN values and conduct Pearson's test between expense and the number of posts
    bad = ~np.logical_or(np.isnan(Expense), np.isnan(NumberOfPosts))
    corr, p_value = pearsonr(np.compress(bad, Expense), np.compress(bad, NumberOfPosts))
    print("The correlation between expense and the number of posts is ", corr, 
      ", and the p-value for Pearson's test is ", p_value, sep = '')
    
    # remove NaN values and conduct Pearson's test between EBITDA and the number of posts
    bad = ~np.logical_or(np.isnan(EBITDA), np.isnan(NumberOfPosts))
    corr, p_value = pearsonr(np.compress(bad, EBITDA), np.compress(bad, NumberOfPosts))
    print("The correlation between EBITDA and the number of posts is ", corr, 
      ", and the p-value for Pearson's test is ", p_value, sep = '')    


# In[4]:


#----------------- Run above functions on given datasets -----------------
# locate datasets
financial_data_file = 'team/courses/MSiA400/GrandCanyon/data/FinancialData.csv'
posting_data_file = 'team/courses/MSiA400/GrandCanyon/data/postingsbyquarter.csv'
FinancialData = pd.read_csv(financial_data_file, encoding = "ISO-8859-1")
PostingsData = pd.read_csv(posting_data_file, encoding = "ISO-8859-1")

# merge datasets
FinanPostsData = MergeFinancialPostings(FinancialData, PostingsData)

# compute and plot correlations, and conduct Pearson's test on the correlations
ScatterPlot(FinanPostsData)
ComputeCorrelation(FinanPostsData)
HeatMap(FinanPostsData)
CorrTest(FinanPostsData)

