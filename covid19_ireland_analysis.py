import pandas as pd
import matplotlib.pyplot as plt
import re

# Dataset path (same folder lo unte)
file_path = r'C:\Users\MYPC\Downloads\P-CDCBULLETIN38TBL2-2A.xlsx'



# Read Excel file, skip metadata rows
df = pd.read_excel(file_path, sheet_name=0, skiprows=10)

# Rename first column as 'Age'
df = df.rename(columns={df.columns[0]: 'Age'})

# Remove empty columns & rows
df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

# Rename columns: 'Age', 'Week_1', 'Week_2', ...
new_columns = ['Age'] + [f'Week_{i}' for i in range(1, len(df.columns))]
df.columns = new_columns

# Filter valid Age rows
age_pattern = r'^\d|Age not stated|^\d{1,2}-\d{1,2}|^\d{1,2}\+$'
df = df[df['Age'].str.match(age_pattern, na=False)]

# Melt dataframe to long format: Age | Week | Deaths
df_long = df.melt(id_vars='Age', var_name='Week', value_name='Deaths')

# Clean Deaths column
df_long['Deaths'] = pd.to_numeric(df_long['Deaths'], errors='coerce').fillna(0)

# Extract Week number
df_long['Week_num'] = df_long['Week'].str.extract(r'(\d+)').astype(int)

# Filter final Age groups (valid ones)
valid_age_pattern = r'^(0-14|15-24|25-44|45-64|65-79|80\+|Age not stated)$'
df_long = df_long[df_long['Age'].str.match(valid_age_pattern, na=False)]


# 2️Data Summary
# Total deaths by Age group
age_summary = df_long.groupby('Age', as_index=False)['Deaths'].sum()

# Total deaths by Week
week_summary = df_long.groupby('Week_num', as_index=False)['Deaths'].sum()

# Print summaries
print("\nDeaths by Age Group:\n", age_summary)
print("\nDeaths by Week:\n", week_summary)


# 3️Plots
#  Bar Chart: Total Deaths by Age Group
plt.figure(figsize=(8,5))
plt.bar(age_summary['Age'], age_summary['Deaths'], color='steelblue')
plt.xlabel('Age Group')
plt.ylabel('Total Deaths')
plt.title('Total COVID-19 Deaths by Age Group in Ireland')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Line Chart: Weekly Deaths
plt.figure(figsize=(10,6))
plt.plot(week_summary['Week_num'], week_summary['Deaths'], marker='o', color='darkred')
plt.xlabel('Week Number')
plt.ylabel('Deaths')
plt.title('Weekly COVID-19 Deaths in Ireland')
plt.grid(True)
plt.tight_layout()
plt.show()


#  Multi-Line Chart: Weekly Deaths by Age Group
plt.figure(figsize=(12,7))
for age_group in df_long['Age'].unique():
    subset = df_long[df_long['Age'] == age_group]
    plt.plot(subset['Week_num'], subset['Deaths'], marker='o', label=age_group)

plt.xlabel('Week Number')
plt.ylabel('Deaths')
plt.title('COVID-19 Deaths by Age Group in Ireland (Weekly)')
plt.legend(title='Age Group')
plt.grid(True)
plt.tight_layout()
plt.show()

