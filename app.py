from datetime import datetime
from platform import python_version
import socket
import platform
import os
from flask import Flask, render_template
from scipy.stats import f_oneway
import numpy as np
import re
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

@app.route('/', methods=['POST', 'GET'])
def index():
    # show table
    data = pd.read_excel("C:/Users/Moreno/OneDrive - ZHAW/Desktop/projectwork_SP_FS2023_group_11/snb2.xlsx")
    table_html = data.head(10).to_html()

    #Connect to the SQLite database
    conn = sqlite3.connect('datenbank_snb2.db')
    cursor = conn.cursor()

    # Execute SQL query for Gold table
    query = "SELECT * FROM Gold"
    cursor.execute(query)
    result_list = cursor.fetchall()

    # Data preparation and table creation for Gold
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
                    amount_formatted = "{:,.2f}".format(float(numeric_value)).replace(",", "'")  # Format with thousands separator
                    other_data.append(amount_formatted)
                else:
                    other_data.append(None)
            else:
                other_data.append(value)

        table_data.append([date] + other_data)

    # Create a pandas DataFrame for Gold
    df1 = pd.DataFrame(table_data, columns=header)
    df1['Amount'] = df1['Amount'].round(2)
    gold_table_html = df1.to_html()

    # Execute SQL query for Total Position
    query = """SELECT 'Gold' AS Table_Name, SUM(Position) AS Total_Position FROM Gold
               UNION ALL
               SELECT 'InternationaleZahlungsmittel' AS Table_Name, SUM(Position) AS Total_Position FROM InternationaleZahlungsmittel
               UNION ALL
               SELECT 'Reserve' AS Table_Name, SUM(Position) AS Total_Position FROM Reserve;"""
    cursor.execute(query)
    result_list = cursor.fetchall()

    # Data preparation and table creation for Total Position
    table_data = []
    header = ["Asset", "Sum"]  # Header for the asset and sum columns

    for row in result_list:
        asset = row[0]  # Assuming the asset name is in the first column of the result
        other_data = []

        # Convert strings to numerical values using regular expressions
        for value in row[1:]:
            if isinstance(value, str):
                # Remove non-digit characters
                numeric_value = re.sub(r'[^\d.]+', '', value)
                if numeric_value:
                    amount_formatted = "{:,.2f}".format(float(numeric_value)).replace(",", "'")  # Format with thousands separator
                    other_data.append(amount_formatted)
                else:
                    other_data.append(None)
            else:
                other_data.append(value)

        table_data.append([asset] + other_data)

    # Create a pandas DataFrame for Total Position
    df2 = pd.DataFrame(table_data, columns=header)
    df2['Sum'] = df2['Sum'].round(2)
    total_position_table_html = df2.to_html()

    # mean, max, min, standard deviation for descriptive analyses
    # List of table names
    table_names = ["Gold", "InternationaleZahlungsmittel", "Reserve", "Währungshilfekredite"]

    # Data preparation and statistics calculation for each table
    statistics = []

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
        mean = np.mean(amounts).round(2)
        max_value = np.max(amounts).round(2)
        min_value = np.min(amounts).round(2)
        std_dev = np.std(amounts).round(2)

        statistics.append({
            'Asset': table_name,
            'Mean': mean,
            'Max': max_value,
            'Min': min_value,
            'Standard Deviation': std_dev
        })

        # Example usage of loop control statements
        if mean > 1000:
            break

        if max_value > 5000:
            continue

    # Connect to the SQLite database again
    conn = sqlite3.connect('datenbank_snb2.db')
    cursor = conn.cursor()

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

    # Graph plot
    data.plot()
    graph_path = 'static/graph.png'
    plt.savefig(graph_path)
    plt.close()

    # Data for Pie-Chart
    data = [
    ['2020-01', 51119.6319, 1357.281079, 4348.52943, 347.6192427],
    ['2020-02', 52291.98641, 1314.623212, 4327.827212, 345.1162577],
    ['2020-03', 51920.26084, 1291.86913, 4164.863706, 476.4898326],
    ['2020-04', 55331.25711, 1664.81605, 4191.570537, 761.6554115]
    ]



    pie_chart_paths = []
    for i, row in enumerate(data):
        row_label = row[0]
        row_data = row[1:]

        # Create the pie chart
        plt.pie(row_data, autopct='%1.1f%%')

        # add title
        plt.suptitle('Verteilung der Aktiven - {}'.format(row_label), ha='left', fontsize=12)

        # Aktivposten-Labels
        labels = ['Gold und Forderungen aus Goldgeschäften', 'Reserveposition beim IWF',
                  'Internationale Zahlungsmittel', 'Währungshilfekredite']

        # Add the title of the active next to the pie chart
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.6))

        # Save the pie chart image
        pie_chart_path = 'static/pie{}.png'.format(i+1)
        plt.savefig(pie_chart_path)
        plt.close()

        pie_chart_paths.append(pie_chart_path)

    # Close the database connection
    conn.close()

    # Get system information
    os_name = os.name.upper()
    system_name = platform.system()
    system_release = platform.release()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    python_version_info = python_version()

    return render_template('index.html', table_html=table_html, gold_table_html=gold_table_html,
                       total_position_table_html=total_position_table_html, statistics=statistics,
                       f_statistic=f_statistic, p_value=p_value, graph_path=graph_path,
                       pie_data=data, pie_chart_paths=pie_chart_paths, os_info=os_name,
                       system_info=system_name, current_datetime=current_datetime,
                       python_version=python_version_info)



app.debug = True
app.run(host='0.0.0.0', port=port)
