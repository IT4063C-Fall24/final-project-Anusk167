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

# In[63]:


## 1) Importing dataset 1 via API Call:
url = 'https://rplumber.ilo.org/data/indicator/?id=UNE_DEAP_SEX_AGE_RT_A&timefrom=1970&type=label&format=.csv'
import pandas as pd
import matplotlib.pyplot as plt
unemployment_data = pd.read_csv(url)
unemployment_data.head(5)

## 2) Importing dataset 2 via open:
with open('assets/Global poverty and inequality dataset/pip_dataset.csv') as glo_poverty:
    glo_poverty = pd.read_csv(glo_poverty, delimiter=',')
    glo_poverty = pd.DataFrame(glo_poverty)
glo_poverty.head(5)

## 3) Importing dataset 3 via open:
with open('assets/HDI/HDI_Full.csv') as hdi_full:
    hdi_full = pd.read_csv(hdi_full, delimiter=',')
    hdi_full = pd.DataFrame(hdi_full)
hdi_full.head(5)


# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->
# I intend to make use of the vast arrays of metrics available in these 3 databases to find trends that either positively or negatively affect global poverty rates. One of the datasets that I'm using is the HDI dataset that has a comprehensive array of metrics, one of which is literacy rate. Along with this dataset, the two other datasets have similar metrics that one would think of as fundamental metrics that might affect the poverty rates. As the project is in its early stages, I don't have a solid roadmap, but I'm confident that I have picked the right datasets that will provide me a wealth of data to perform my analysis on.

# In[78]:


# Getting distribution on all three datasets

display(glo_poverty.describe(), unemployment_data.describe(), hdi_full.describe())


# In[80]:


# Getting information on all three datasets

display(glo_poverty.info(), "\n", unemployment_data.info(), "\n", hdi_full.info())


# In[34]:


###Finding the min and max value for 'year' to filter data based on availability.

### glo_poverty Max: 2021 Min: 1967
glo_poverty = glo_poverty.rename(columns={'year':'date'})
display((glo_poverty.sort_values(by='date')).head(1),(glo_poverty.sort_values(by='date', ascending=False)).head(1))

### unemployment_data Max: 2023 Min: 1970
unemployment_data = unemployment_data.rename(columns={'time':'date'})
display(unemployment_data.sort_values(by='date').head(1), unemployment_data.sort_values(by='date', ascending=False).head(1))

### hdi_full Max: 2021 Min: 1991
hdi = hdi_full.melt(id_vars='Country', value_name='HDI', value_vars=hdi_full.columns[6:37])
hdi['variable'] = hdi['variable'].str.replace("Human Development Index ", '', regex=True).str[1:-1]
hdi = hdi.rename(columns={'variable':'date'})
hdi['date'] = hdi['date'].astype('float64')
display(hdi.sort_values(by='date').head(1), hdi.sort_values(by='date', ascending=False).head(1))



# In[35]:


### Filtering all dataframes to only include the dates present in all three dataframes
glo_poverty = glo_poverty[(glo_poverty['date'] >= 1991) & (glo_poverty['date'] <= 2021)]
unemployment_data = unemployment_data[(unemployment_data['date'] >= 1991) & (unemployment_data['date'] <= 2021)]

### Verifying that all dataframes have the same min and max values for the 'date' column
display(
glo_poverty['date'].describe().loc[['min', 'max']],
unemployment_data['date'].describe().loc[['min', 'max']],
hdi['date'].describe().loc[['min', 'max']])


# In[48]:


### Filtering datasets to only keep relevant records

### Experimenting with 'national' as the filtering value for the field 'reporting level' as national level reports tend to be more accurate than rural or urban level
glo_poverty_final = glo_poverty[glo_poverty['reporting_level'] == "national"]
display(glo_poverty_final['country'].nunique(), glo_poverty['country'].nunique(), glo_poverty_final['welfare_type'].unique())
### With a loss of only 10 nations (167 from 177) in the new dataframe, this loss is worth data that is going to be more accurate.




# In[59]:


unemployment_data.head()
unemployment_data['source.label'].unique()
unemployment_data = unemployment_data[(unemployment_data['source.label'] == 'LFS - Labour Force Survey') & (unemployment_data['sex.label'] == 'Sex: Total')
& (unemployment_data['classif1.label'] == 'Age (Aggregate bands): Total')]

display(unemployment_data.sort_values(by=['ref_area.label', 'date']).head(100))


# In[72]:


### A line chart showing the trend of HDI in all countries with data available. Overall, we can see that a positive trend in the global scale.
plt.figure(figsize=(8, 6))
for country, group_data in hdi.groupby('Country'):
    plt.plot(group_data['date'], group_data['HDI'], label=country)

plt.show()


# In[77]:


# Comparing the last figure with HDI trend overtime for the countries with the top 10 countries with the least HDI values in 1991, we can see
# that the trend is positive as well. This shows that HDI is increasing in a global scale.
hdi_below_average = hdi[(hdi['date'] == 1991)]
hdi_below_average = hdi_below_average[(hdi_below_average['HDI'] <= hdi_below_average['HDI'].mean())].sort_values(by='HDI').head(10)

plt.figure(figsize=(8, 6))
hdi_below_average = hdi[hdi['Country'].isin(hdi_below_average['Country'])]
display(hdi_below_average.head(20))

for country, group_data in hdi_below_average.groupby('Country'):
    plt.plot(group_data['date'], group_data['HDI'], label=country)

plt.show()


# In[ ]:





# - All in all, the basic filtering and transformations have been made on all three dataframes. I have not included visuals as I am still working on integrating the datasets together. So far, the common fields that I can use to integrate these three dataframes are location and date. 
# 
# - The null values in all dataframes are un-imputable because of the nature of the data and sparsely exist to begin with. So i have decided to drop them.
# 
# - I haven't received any feedback from my peers so I have not made any changes based on peer feedback.

# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->
# - Stack overflow

# In[61]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

