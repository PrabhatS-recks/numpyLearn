# Pandas Data Manipulation & Analysis with Python

A step-by-step repository demonstrating data cleaning, feature engineering, boolean filtering, datetime extraction, and aggregation using **Pandas** and an **Employee Performance & Salary** dataset (`employee_data.csv`).

---

## 📌 Project Overview

This project provides a practical implementation of core Pandas data manipulation workflows, structured around standard data analysis notes:

1. **Inspection & Cleaning**: Handling missing values using median/mean imputation.
2. **Data Selection & Filtering**: Using label-based (`loc`), position-based (`iloc`), and complex boolean indexing.
3. **Feature Engineering**: Creating conditional columns with `numpy.where()` and `.apply()` with lambda functions.
4. **GroupBy Aggregations**: Computing summary statistics (Split-Apply-Combine pattern) per department.
5. **Datetime Processing**: Converting dates and extracting temporal features (`.dt` accessor).
6. **Data Export**: Sorting and saving clean datasets without extra index columns.

---

## 🛠️ Project Structure

```text
├── employee_data.csv         # Raw sample dataset (500 rows)
├── employee_analysis.py      # Main Pandas execution script
├── cleaned_employee_data.csv # Output generated after analysis
├── .gitignore                # Ignores virtual environments and cache
└── README.md                 # Project documentation