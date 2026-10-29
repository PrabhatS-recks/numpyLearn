import pandas as pd
import numpy as np

df=pd.read_csv('employee_data.csv')

print("\n--- 9 & 3. SORTING & EXPORTING ---")

# Sort values by Department (ascending) and Salary (descending)
sorted_df = df.sort_values(
    by=['Department', 'Salary'], 
    ascending=[True, False]
)

print("Top 3 rows of the sorted DataFrame:")
print(sorted_df[['Department', 'Name', 'Salary']].head(3))

# Export the final transformed DataFrame to a new CSV file
sorted_df.to_csv('cleaned_employee_data.csv', index=False)
print("\nSuccess! Cleaned and sorted data exported to 'cleaned_employee_data.csv'.")