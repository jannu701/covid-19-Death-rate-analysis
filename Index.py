import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore') 
# Example: Reading data from a CSV file
df = pd.read_csv('data/india_cases.csv')

# Display the first few rows of the DataFrame
print(df.head())

# Get information about the DataFrame
print(df.info())

# Summary statistics of the DataFrame
print(df.describe())
# Check for missing values
print(df.isnull().sum())

# Handle missing values (e.g., impute or remove)
# Example: Remove rows with any missing values
df_cleaned = df.dropna()
print(df.duplicated().sum())

# Remove duplicates
df_cleaned = df.drop_duplicates()
# Example: Convert date column to datetime format
df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])

# Example: Convert text to lowercase for consistency
df_cleaned['State/UnionTerritory'] = df_cleaned['State/UnionTerritory'].str.lower()

# Example: Export cleaned data to a new CSV fileclear
df_cleaned.to_csv('cleaned_covid_data.csv', index=False)
