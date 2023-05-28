from datetime import datetime
from platform import python_version
import socket
import platform
import os
from scipy.stats import f_oneway
import numpy as np
import re
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# show table
data = pd.read_excel(
    "C:/Users/Moreno/OneDrive - ZHAW/Desktop/projectwork_SP_FS2023_group_11/snb2.xlsx")

print("\n")
print(data.head(10))

# dataframe

#Connect to the SQLite database
conn = sqlite3.connect('datenbank_snb2.db')
cursor = conn.cursor()

# Execute SQL query
query = "SELECT * FROM Gold"  
cursor.execute(query)
result_list = cursor.fetchall()

# Data preparation and table creation
table_data = []
header = ["Date", "Amount"]  # Header for the date and amount columns

for row in result_list:
    date = row[0]  # Assuming the date is in the first column of the result
    other_data = []

    # Convert strings to numerical values using regular expressions
    for value in row[1:]:
        if isinstance(value, str):
            # Remove non-digit characters
            numeric_value = re.sub(r'[^\d.]+', '', value)
            if numeric_value:
                amount_formatted = "{:,.2f}".format(float(numeric_value)).replace(
                    ",", "'")  # Format with thousands separator
                other_data.append(amount_formatted)

            else:
                other_data.append(None)
        else:
            other_data.append(value)

    table_data.append([date] + other_data)

# Create a pandas DataFrame
df1 = pd.DataFrame(table_data, columns=header)

# Round the "Amount" column to two decimal places
df1['Amount'] = df1['Amount'].round(2)

print("\n")
print("Asset: Gold")

# Set the default display format for float values
pd.options.display.float_format = "{:,.2f}".format
print(df1)


#Connect to the SQLite database
conn = sqlite3.connect('datenbank_snb2.db')
cursor = conn.cursor()

# Execute SQL query
query = """SELECT 'Gold' AS Table_Name, SUM(Position) AS Total_Position FROM Gold
UNION ALL
SELECT 'InternationaleZahlungsmittel' AS Table_Name, SUM(Position) AS Total_Position FROM InternationaleZahlungsmittel
UNION ALL
SELECT 'Reserve' AS Table_Name, SUM(Position) AS Total_Position FROM Reserve;
"""
cursor.execute(query)
result_list = cursor.fetchall()

# Data preparation and table creation
table_data = []
header = ["Asset", "Sum"]  # Header for the date and amount columns

for row in result_list:
    date = row[0]  # Assuming the date is in the first column of the result
    other_data = []

    # Convert strings to numerical values using regular expressions
    for value in row[1:]:
        if isinstance(value, str):
            # Remove non-digit characters
            numeric_value = re.sub(r'[^\d.]+', '', value)
            if numeric_value:
                amount_formatted = "{:,.2f}".format(float(numeric_value)).replace(
                    ",", "'")  # Format with thousands separator
                other_data.append(amount_formatted)

            else:
                other_data.append(None)
        else:
            other_data.append(value)

    table_data.append([date] + other_data)

# Create a pandas DataFrame
df2 = pd.DataFrame(table_data, columns=header)

# Round the "Amount" column to two decimal places
df2['Sum'] = df2['Sum'].round(2)


# Set the default display format for float values
pd.options.display.float_format = "{:,.2f}".format
print("\n")
print(df2)


# mean, max, min, standardabweichung for descriptive analyses
#Connect to the SQLite database
conn = sqlite3.connect('datenbank_snb2.db')
cursor = conn.cursor()

# List of table names
table_names = ["Gold", "InternationaleZahlungsmittel",
               "Reserve", "Währungshilfekredite"]

# Data preparation and statistics calculation for each table
for table_name in table_names:
    # Assuming there's a column 'JahrMonat' for the date
    query = f"SELECT JahrMonat, Position FROM {table_name}"
    cursor.execute(query)
    result_list = cursor.fetchall()

    dates = []
    amounts = []

    for row in result_list:
        dates.append(row[0])
        value = row[1]
        if isinstance(value, str):
            # Remove non-digit characters
            numeric_value = re.sub(r'[^\d.]+', '', value)
            if numeric_value:
                amounts.append(float(numeric_value))
            else:
                amounts.append(None)
        else:
            amounts.append(value)

    # Calculate statistics for the amounts column
    amounts = np.array(amounts)
    mean = np.mean(amounts)
    max_value = np.max(amounts)
    min_value = np.min(amounts)
    std_dev = np.std(amounts)

    print("\n")

    # Print the statistics results for the table
    print(f"Asset: {table_name}")
    print("Mean:", mean.round(2))
    print("Max:", max_value.round(2))
    print("Min:", min_value.round(2))
    print("Standard Deviation:", std_dev.round(2))
    print()

 # Example usage of loop control statements
    if mean > 1000:
        print("Mean is greater than 1000. Exiting the loop.")
        break

    if max_value > 5000:
        print("Maximum value is greater than 5000. Skipping this table.")
        pass

print("\n")

# Connect to the SQLite database
conn = sqlite3.connect('datenbank_snb2.db')
cursor = conn.cursor()

# List of table names
table_names = ["Gold", "InternationaleZahlungsmittel",
               "Reserve", "Währungshilfekredite"]

# Data preparation and statistics calculation for each table
table_data = []

for table_name in table_names:
    query = f"SELECT Position FROM {table_name}"
    cursor.execute(query)
    result_list = cursor.fetchall()

    amounts = []

    for row in result_list:
        value = row[0]
        if isinstance(value, str):
            # Remove non-digit characters
            numeric_value = re.sub(r'[^\d.]+', '', value)
            if numeric_value:
                amounts.append(float(numeric_value))
            else:
                amounts.append(None)
        else:
            amounts.append(value)

    # Store the amounts column in the table_data list
    table_data.append(amounts)

# Perform ANOVA test
f_statistic, p_value = f_oneway(*table_data)

# Print the ANOVA results
print("ANOVA F-Statistic:", f_statistic)
print("ANOVA p-value:", p_value)


# graph plotten
data.plot()

plt.show()


# Daten for Pie-Chart
data = [
    ['2020-01', 51119.6319, 1357.281079, 4348.52943, 347.6192427],
    ['2020-02', 52291.98641, 1314.623212, 4327.827212, 345.1162577],
    ['2020-03', 51920.26084, 1291.86913, 4164.863706, 476.4898326],
    ['2020-04', 55331.25711, 1664.81605, 4191.570537, 761.6554115]
]


# Loop over the data and create a pie chart for each row
for row in data:
    row_label = row[0]
    row_data = row[1:]

    # Create the pie chart
    plt.pie(row_data, autopct='%1.1f%%')

    # add title
    plt.suptitle('Verteilung der Aktiven - {}'.format(row_label),
                 ha='left', fontsize=12)

    # Aktivposten-Labels
    labels = ['Gold und Forderungen aus Goldgeschäften', 'Reserveposition beim IWF',
              'Internationale Zahlungsmittel', 'Währungshilfekredite']

    # Add the title of the active next to the pie chart
    plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.6))

    # Save the pie chart image
    plt.savefig('static/pie{}.png'.format(i+1))
    plt.close()

    # show pie chart
    plt.show()

# Close the database connection
conn.close()

print('-----------------------------------')
print(os.name.upper())
print(platform.system(), '|', platform.release())
print('Datetime:', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('Python Version:', python_version())
print('-----------------------------------')
