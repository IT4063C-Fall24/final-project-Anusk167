#!/usr/bin/env python
# coding: utf-8

# # Global Poverty
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# 📝 <!-- Answer Below -->
# 
# I am trying to observe trends in global poverty rates and identify trends and patterns in events that caused a significant shift in poverty rates, for better or for worse.

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
# 📝 <!-- Answer Below -->
# 
# What are some large scale events that trigger a shift in poverty rates across the global populus? 

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# 📝 <!-- Answer Below -->
# 
# Identifying significant events, whether they are economic, political natural, etc., and finding a pattern in such events that have been heavily linked with swaying the global poverty rate. 

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 📝 <!-- Answer Below -->
# 
# -1 ILOSTAT - Unemployment rate by sex and age (%) - Annual
# -2 Kaggle (Source: World Bank) - Global poverty and inequality dataset
# 
# 
# 

# In[3]:


## 1) Importing dataset 1 via API Call:
url = 'https://rplumber.ilo.org/data/indicator/?id=UNE_DEAP_SEX_AGE_RT_A&timefrom=1970&type=label&format=.json'
import requests as rq
import pandas as pd

data = rq.get(url)

data = pd.DataFrame.from_records(data.json()[1:], columns=[0])

data.head(5)




# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->

# In[1]:


# Start your code here


# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->

# In[2]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

