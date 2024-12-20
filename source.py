#!/usr/bin/env python
# coding: utf-8

# # Global Poverty
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# 📝 <!-- Answer Below -->
# 
# I am trying to observe how well HDI and Unemployment rates perform as predictors for Global Poverty

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
# 📝 <!-- Answer Below -->
# <ul>
# - What is the relationship between HDI (Human Development Index) and Poverty Rate?<br>
# - Does the Unemployment Rate significantly impact Poverty Rate?<br>
# - Can we predict Poverty Rate using HDI, Unemployment Rate, or a combination of these variables?
# </ul>

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# 📝 <!-- Answer Below -->
# 
# - HDI and Unemployment are(inversely/ directly) proportional to Global Poverty. While 'X' seems to have a minor correlation to the target variable, 'Y' seems to be a strong indicator of the target variable

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

# In[53]:


import pandas as pd
import matplotlib.pyplot as plt

## 1) Importing dataset 1 via API Call:
# url = 'https://rplumber.ilo.org/data/indicator/?id=UNE_DEAP_SEX_AGE_RT_A&timefrom=1970&type=label&format=.csv'

# unemployment_data = pd.read_csv(url)
# unemployment_data.head(5)

## The link is now corrupted

with open('assets/Unemployment/Unemployment.csv', encoding='utf-8-sig') as unemployment_data:
    unemployment_data = pd.read_csv(unemployment_data, delimiter=',')
    unemployment_data = pd.DataFrame(unemployment_data)


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
unemployment_data.head(5)


# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->
# I intend to make use of the vast arrays of metrics available in these 3 databases to find trends that either positively or negatively affect global poverty rates. One of the datasets that I'm using is the HDI dataset that has a comprehensive array of metrics, one of which is literacy rate. Along with this dataset, the two other datasets have similar metrics that one would think of as fundamental metrics that might affect the poverty rates. As the project is in its early stages, I don't have a solid roadmap, but I'm confident that I have picked the right datasets that will provide me a wealth of data to perform my analysis on.

# In[54]:


# Getting distribution on all three datasets

display(glo_poverty.describe(), unemployment_data.describe(), hdi_full.describe())


# In[55]:


# Getting information on all three datasets

display(glo_poverty.info(), "\n", unemployment_data.info(), "\n", hdi_full.info())


# In[56]:


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



# In[57]:


### Filtering all dataframes to only include the dates present in all three dataframes
glo_poverty = glo_poverty[(glo_poverty['date'] >= 1991) & (glo_poverty['date'] <= 2021)]
unemployment_data = unemployment_data[(unemployment_data['date'] >= 1991) & (unemployment_data['date'] <= 2021)]

### Verifying that all dataframes have the same min and max values for the 'date' column
display(
glo_poverty['date'].describe().loc[['min', 'max']],
unemployment_data['date'].describe().loc[['min', 'max']],
hdi['date'].describe().loc[['min', 'max']])


# In[58]:


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


# In[60]:


### A line chart showing the trend of HDI in all countries with data available. Overall, we can see that a positive trend in the global scale.
plt.figure(figsize=(8, 6))
for country, group_data in hdi.groupby('Country'):
    plt.plot(group_data['date'], group_data['HDI'], label=country)

plt.show()


# In[61]:


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


# - All in all, the basic filtering and transformations have been made on all three dataframes. I have not included visuals as I am still working on integrating the datasets together. So far, the common fields that I can use to integrate these three dataframes are location and date. 
# 
# - The null values in all dataframes are un-imputable because of the nature of the data and sparsely exist to begin with. So i have decided to drop them.
# 
# - I haven't received any feedback from my peers so I have not made any changes based on peer feedback.

# <b> Checkpoint 3 </b> <br>
# <b>Part 1:</b><br>
# <b>Machine Learning Plan:</b> <br><br>
# 
# - For this project, I plan to use Linear Regression or Polynomial Regression as the primary machine learning models. These are well-suited for predicting one metric (e.g., Poverty) based on the other metrics (HDI, Unemployment Rate) and for exploring relationships between variables. Additionally, I will create a correlation matrix to analyze how these variables are related.
# 
# - As for the challenges, I have noted these for now: <br> <ul><li>Metrics like HDI, Unemployment Rate, and Poverty may have strong correlations with each other, which could make it difficult to isolate the effect of one variable on another.</li><li>Relationships between these metrics might not be purely linear, which could reduce the accuracy of a basic Linear Regression model.</li><li>Outliers or regions with extreme values could skew the model's predictions.</li></ul> 
# 
# - I have also come up with some solutions to these problems. They are: <ul><li>I will compare the performance of Linear Regression and Polynomial Regression models to determine which best fits the data.</li><li>Before applying any model, I will visualize the data distribution (e.g., using scatter plots) to identify outliers. If necessary, I’ll explore transformations or filtering methods to reduce their impact.</li><li>I will focus on interpreting the regression coefficients and the overall model accuracy (e.g., using R² values) to ensure the results align with real-world expectations.</li></ul>
# 
# 
# 
# 

# <b>Part 2: </b>
# <br><br>
# <b>EDA:</b>

# In[62]:


display(glo_poverty_final.info(), hdi.info(), unemployment_data.info())

#Figuring out what unique values the "obs_status.label" column contains in the "unemployment_data" dataframe
print(unemployment_data['obs_status.label'].unique())

#Filtering out records with "Break in series" and "Unreliable" values as these are placeholders.
unemployment_final = unemployment_data[['ref_area.label', 'date', 'obs_value']]
unemployment_final.rename(columns={'ref_area.label': 'Country', 'obs_value': 'Unemployment_rate'}, inplace= True)

#Removing all null values as Annual HDI value is a key metric and imputation is not advised.
hdi = hdi[hdi['HDI'].notnull()]


#Filtererd and renamed columns for glo_poverty_final
glo_poverty_final = glo_poverty_final[glo_poverty_final['welfare_type'] == 'income']
glo_poverty_final = glo_poverty_final[['country', 'date', 'headcount_ratio_upper_mid_income_povline']]
glo_poverty_final.rename(columns ={'headcount_ratio_upper_mid_income_povline' : 'Poverty_rate', 'country' : 'Country'}, inplace=True)
glo_poverty_final.head()



# In[63]:


display(hdi.head(), unemployment_final.head(), glo_poverty_final.head())


# In[64]:


import seaborn as sns
sns.histplot(hdi['HDI'], kde=True)


# In[65]:


sns.histplot(unemployment_final['Unemployment_rate'], kde=True)


# In[66]:


sns.histplot(glo_poverty_final['Poverty_rate'], kde=True)


# In[67]:


merged_df = pd.merge(hdi, unemployment_final, on=['Country', 'date'], how='inner')
final_df = pd.merge(merged_df, glo_poverty_final, on=['Country', 'date'], how='inner')
final_df.head()


# In[68]:


corr_matrix = final_df[['HDI', 'Unemployment_rate', 'Poverty_rate']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')


# - Scatter plots

# In[69]:


import seaborn as sns
sns.pairplot(hdi, diag_kind='kde', markers='+')
plt.show()


# In[70]:


sns.pairplot(unemployment_final, diag_kind='kde', markers='+')
plt.show()


# In[71]:


sns.pairplot(glo_poverty_final, diag_kind='kde', markers='+')
plt.show()


# <b>Prepare</b>

# In[72]:


from sklearn.model_selection import train_test_split
#Not using random split as we have a temporal component (date) that reflects yearly progression
final_df = final_df.sort_values(by='date')
train_data = final_df[final_df['date'] < 2012]
test_data = final_df[final_df['date'] >= 2012]
X_train, y_train = train_data[['HDI', 'Unemployment_rate']], train_data['Poverty_rate']
X_test, y_test = test_data[['HDI', 'Unemployment_rate']], test_data['Poverty_rate']



# - <b>Pipelines</b>

# In[73]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import root_mean_squared_error, r2_score

# Defining numerical and categorical columns
numerical_columns = ['HDI', 'Unemployment_rate', 'Poverty_rate']
categorical_columns = ['Country']

# Creating pipeline
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),  
        ('cat', OneHotEncoder(), categorical_columns)
    ],
    remainder='passthrough' 
)

# Apply the pipeline
df_cleaned_encoded = preprocessing_pipeline.fit_transform(final_df)



# - Analysis

# In[74]:


# Applying Linear regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred_linear = linear_model.predict(X_test)
linear_r2 = r2_score(y_test, y_pred_linear)
linear_mse = root_mean_squared_error(y_test, y_pred_linear)

# Applying Polynomial Regression (degree 2)
degree = 2
poly_features = PolynomialFeatures(degree=degree)
X_poly_train = poly_features.fit_transform(X_train)
X_poly_test = poly_features.transform(X_test)
poly_model = LinearRegression()
poly_model.fit(X_poly_train, y_train)
y_pred_poly = poly_model.predict(X_poly_test)
poly_r2 = r2_score(y_test, y_pred_poly)
poly_mse = root_mean_squared_error(y_test, y_pred_poly)


# In[75]:


results = {
    'Model': ['Linear Regression', 'Polynomial'],
    'R2 Score': [linear_r2, poly_r2],
    'RMSE': [linear_mse, poly_mse]
}
results_df = pd.DataFrame(results)
display(results_df)


# - <b>Our analysis indicates that HDI is inversely correlated with Poverty Rate, suggesting that improving HDI could reduce poverty levels. Unemployment Rate, however, showed a weaker relationship, indicating that other factors may also play a significant role.</b>

# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->
# - Stack overflow
# - ChatGPT for building column transformers

# In[76]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

